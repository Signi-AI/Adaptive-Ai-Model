
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4


@dataclass
class Attempt:
    """
    One student submission for a generated question.

    Stored after the answer engine evaluates the response.
    """
    id: str
    question_id: str
    student_id: str
    submitted_answer: Any
    expected_answer: Any
    is_correct: bool
    feedback: str
    tolerance_used: Optional[float] = None
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)



    @classmethod
    def create(
        cls,
        question_id: str,
        student_id: str,
        submitted_answer: Any,
        expected_answer: Any,
        is_correct: bool,
        feedback: str,
        tolerance_used: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "Attempt":
        return cls(
            id=str(uuid4()),
            question_id=question_id,
            student_id=student_id,
            submitted_answer=submitted_answer,
            expected_answer=expected_answer,
            is_correct=is_correct,
            feedback=feedback,
            tolerance_used=tolerance_used,
            metadata=metadata or {},
        )


class AttemptStore:
    """In-memory store for attempts (swap for DB in production)."""

    def __init__(self):
        self._items: Dict[str, Attempt] = {}

    def save(self, attempt: Attempt) -> None:
        self._items[attempt.id] = attempt

    def get(self, attempt_id: str) -> Optional[Attempt]:
        return self._items.get(attempt_id)

    def list_by_question(self, question_id: str) -> List[Attempt]:
        return [a for a in self._items.values() if a.question_id == question_id]

    def list_by_student(self, student_id: str) -> List[Attempt]:
        return [a for a in self._items.values() if a.student_id == student_id]

    def all(self) -> List[Attempt]:
        return list(self._items.values())

    def clear(self) -> None:
        self._items.clear()


default_attempt_store = AttemptStore()