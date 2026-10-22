"""Artificial Teacher orchestration: context in, teaching response out.

This service does NOT touch the database. The backend builds a TeachingRequest from its own
services (student, progress, recommendation, assessment) and sends it to the model server
(artificial_teacher/server.py), which calls respond(). Authoritative
facts (mastery, correctness, recommended action) are inputs, never outputs.
"""
from __future__ import annotations

import logging
import re
import time
from typing import Literal

from pydantic import BaseModel, Field

from artificial_teacher.gemma_client import GemmaClient
from artificial_teacher.prompt_builder import build_messages, build_system_prompt
from artificial_teacher.retrieval_service import RetrievalService
from artificial_teacher.student_context import (
    AssessmentResult,
    Language,
    StudentContext,
    Turn,
    default_teaching_language,
)

log = logging.getLogger(__name__)

MAX_MESSAGE_CHARS = 2000

_LEAK_RETRY_NOTE = (
    "\n\n[System note: your previous draft stated the final answer. Rewrite it as a hint only, "
    "without stating the final answer, and end with exactly one question.]"
)


class TeachingRequest(BaseModel):
    subject: str = Field(..., min_length=1, max_length=100)
    topic: str = Field(..., min_length=1, max_length=150)
    student: StudentContext
    message: str = Field(default="", max_length=10_000)
    history: list[Turn] = Field(default_factory=list)
    assessment: AssessmentResult | None = None
    teaching_language: Language | None = None


class SourceRef(BaseModel):
    chunk_id: str
    source: str
    topic: str | None
    page_start: int
    page_end: int
    scope: Literal["topic", "subject"]


class TeachingResponse(BaseModel):
    response: str
    teaching_mode: str
    language: Language
    grounded: bool  # True when curriculum excerpts were supplied to the model
    sources: list[SourceRef]
    model: str
    latency_ms: int
    warnings: list[str] = Field(default_factory=list)


def leaks_answer(text: str, answer: str) -> bool:
    """Does the reply state the verified final answer? Deliberately conservative."""
    ans = re.sub(r"\s+", "", answer.casefold())
    if not ans:
        return False
    body = text.casefold()
    if re.fullmatch(r"-?\d+(?:[.,/]\d+)?", ans):
        # A bare number appears in many harmless places ("step 3"), so only flag it when stated as a result.
        pattern = (
            r"(?:=|\banswer\s+is|\banswer:|\bjibu\s+ni|\bjibu:|\bequals|\bis)\s*"
            + re.escape(ans)
            + r"(?!\d|[.,/]\d)"
        )
    else:
        # Spaces are optional between any two characters, so "x = 3", "x=3" and "x =3" all match.
        pattern = r"(?<!\w)" + r"\s*".join(re.escape(ch) for ch in ans) + r"(?!\w)"
    return re.search(pattern, body) is not None


class ArtificialTeacherService:
    def __init__(self, client: GemmaClient, retriever: RetrievalService, top_k: int = 4) -> None:
        self._client = client
        self._retriever = retriever
        self._top_k = top_k

    @property
    def model_name(self) -> str:
        return self._client.model

    @property
    def chunks_loaded(self) -> int:
        return self._retriever.chunk_count

    def health(self) -> dict:
        return {**self._client.health(), "model": self._client.model, "chunks_loaded": self._retriever.chunk_count}

    @staticmethod
    def _effective_message(req: TeachingRequest) -> str:
        msg = (req.message or "").strip()
        if not msg and req.assessment:
            msg = f"My answer is: {req.assessment.student_answer}"
        if not msg:
            raise ValueError("Student message is empty and there is no assessment result to respond to.")
        return msg[:MAX_MESSAGE_CHARS]

    def respond(self, req: TeachingRequest) -> TeachingResponse:
        started = time.perf_counter()
        message = self._effective_message(req)
        language: Language = req.teaching_language or default_teaching_language(
            req.student.class_level, req.subject
        )

        hits = self._retriever.retrieve(
            subject=req.subject,
            class_level=req.student.class_level,
            topic=req.topic,
            query=message,
            k=self._top_k,
        )
        system_prompt, action, recognised = build_system_prompt(
            subject=req.subject,
            topic=req.topic,
            student=req.student,
            language=language,
            hits=hits,
            assessment=req.assessment,
        )
        messages = build_messages(system_prompt=system_prompt, history=req.history, user_message=message)

        warnings: list[str] = []
        if not recognised:
            warnings.append(f"unknown_recommended_action:{req.student.recommended_action}")
        if not hits:
            warnings.append("no_curriculum_excerpts")

        text = self._client.chat(messages)

        a = req.assessment
        if a and a.verified_answer and not a.reveal_answer and leaks_answer(text, a.verified_answer):
            retry = [dict(m) for m in messages]
            retry[-1]["content"] += _LEAK_RETRY_NOTE
            text = self._client.chat(retry)
            if leaks_answer(text, a.verified_answer):
                warnings.append("possible_answer_leak")
                log.warning("Teacher reply may still reveal the verified answer after one retry.")

        return TeachingResponse(
            response=text,
            teaching_mode=action,
            language=language,
            grounded=bool(hits),
            sources=[
                SourceRef(
                    chunk_id=h.chunk.id,
                    source=h.chunk.source,
                    topic=h.chunk.topic,
                    page_start=h.chunk.page_start,
                    page_end=h.chunk.page_end,
                    scope=h.scope,  # type: ignore[arg-type]
                )
                for h in hits
            ],
            model=self._client.model,
            latency_ms=int((time.perf_counter() - started) * 1000),
            warnings=warnings,
        )
