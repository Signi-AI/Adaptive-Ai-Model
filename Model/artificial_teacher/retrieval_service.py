"""Offline retrieval over the ingested Tanzania textbooks.

How it works
1. scripts/ingest_content.py writes data/processed/chunks.jsonl.
2. This service loads it once and builds a small BM25 index per (subject, class, topic)
   and per (subject, class).
3. retrieve() ALWAYS filters by subject + class first, then by topic when the topic exists,
   and only then ranks by relevance to the student's message. A Form 2 student never gets
   Form 4 text just because the words match.

No model download, no GPU, no internet. Works for English and Kiswahili because it matches
words, not meaning. Upgrade path (only after the evaluation set says you need it): add a
multilingual embedding model and fuse its ranking with this one.
"""
from __future__ import annotations

import json
import logging
import math
import os
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from artificial_teacher.settings import resolve_path

log = logging.getLogger(__name__)

_TOKEN_RE = re.compile(r"[^\W_]+", re.UNICODE)


def tokenize(text: str) -> list[str]:
    return [t for t in _TOKEN_RE.findall(text.casefold()) if len(t) > 1 or t.isdigit()]


def norm_label(value: object) -> str:
    return " ".join(str(value or "").split()).casefold()


@dataclass(frozen=True)
class Chunk:
    id: str
    text: str
    subject: str
    class_level: str
    topic: str | None
    language: str
    source: str
    page_start: int
    page_end: int


@dataclass(frozen=True)
class RetrievedChunk:
    chunk: Chunk
    score: float
    scope: str  # "topic" = from the selected topic, "subject" = fallback from the same subject+class


class _BM25:
    """Tiny BM25 (Lucene-style idf, always positive). Fine for thousands of chunks."""

    def __init__(self, docs: list[list[str]], k1: float = 1.5, b: float = 0.75) -> None:
        self.k1, self.b = k1, b
        self.docs = docs
        self.n = len(docs)
        self.avgdl = (sum(len(d) for d in docs) / self.n) if self.n else 0.0
        self.tf = [Counter(d) for d in docs]
        df: Counter[str] = Counter()
        for d in docs:
            df.update(set(d))
        self.idf = {t: math.log(1 + (self.n - c + 0.5) / (c + 0.5)) for t, c in df.items()}

    def scores(self, query: list[str]) -> list[float]:
        uniq = set(query)
        out = [0.0] * self.n
        for i, (tf, doc) in enumerate(zip(self.tf, self.docs)):
            norm = self.k1 * (1 - self.b + self.b * len(doc) / self.avgdl) if self.avgdl else self.k1
            s = 0.0
            for t in uniq:
                f = tf.get(t)
                if f:
                    s += self.idf[t] * f * (self.k1 + 1) / (f + norm)
            out[i] = s
        return out


class _Index:
    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks
        self.bm25 = _BM25([tokenize(c.text) for c in chunks])


class RetrievalService:
    def __init__(self, chunks_path: str | Path | None = None) -> None:
        self.path = resolve_path(chunks_path or os.getenv("CONTENT_CHUNKS_PATH", "data/processed/chunks.jsonl"))
        self._topic_idx: dict[tuple[str, str, str], _Index] = {}
        self._scope_idx: dict[tuple[str, str], _Index] = {}
        self.chunk_count = 0
        self._loaded_mtime_ns: int | None = None
        self.load()

    def _current_mtime_ns(self) -> int | None:
        try:
            return self.path.stat().st_mtime_ns
        except FileNotFoundError:
            return None

    def _reload_if_changed(self) -> None:
        """Use newly ingested books without making an operator restart the server."""
        if self._current_mtime_ns() != self._loaded_mtime_ns:
            self.load()

    def load(self) -> None:
        self._topic_idx, self._scope_idx, self.chunk_count = {}, {}, 0
        if not self.path.exists():
            log.warning("No chunks file at %s. The teacher will run WITHOUT curriculum excerpts.", self.path)
            self._loaded_mtime_ns = None
            return
        by_topic: dict[tuple[str, str, str], list[Chunk]] = {}
        by_scope: dict[tuple[str, str], list[Chunk]] = {}
        with self.path.open(encoding="utf-8") as fh:
            for line_no, line in enumerate(fh, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                    chunk = Chunk(
                        id=d["id"], text=d["text"], subject=d["subject"], class_level=d["class_level"],
                        topic=d.get("topic"), language=d.get("language", ""), source=d.get("source", ""),
                        page_start=int(d.get("page_start", 0)), page_end=int(d.get("page_end", 0)),
                    )
                except (ValueError, KeyError) as exc:
                    log.warning("Skipping bad chunk on line %d of %s: %s", line_no, self.path, exc)
                    continue
                scope_key = (norm_label(chunk.subject), norm_label(chunk.class_level))
                by_scope.setdefault(scope_key, []).append(chunk)
                if chunk.topic:
                    by_topic.setdefault(scope_key + (norm_label(chunk.topic),), []).append(chunk)
                self.chunk_count += 1
        self._topic_idx = {k: _Index(v) for k, v in by_topic.items()}
        self._scope_idx = {k: _Index(v) for k, v in by_scope.items()}
        self._loaded_mtime_ns = self._current_mtime_ns()
        log.info("Loaded %d chunks from %s", self.chunk_count, self.path)

    def coverage(self, subject: str, class_level: str, topic: str | None) -> dict[str, int]:
        """How much text do we actually have? Use this to diagnose 'the AI knows nothing about X'."""
        self._reload_if_changed()
        scope_key = (norm_label(subject), norm_label(class_level))
        topic_idx = self._topic_idx.get(scope_key + (norm_label(topic),))
        scope_idx = self._scope_idx.get(scope_key)
        return {
            "topic_chunks": len(topic_idx.chunks) if topic_idx else 0,
            "subject_chunks": len(scope_idx.chunks) if scope_idx else 0,
        }

    def retrieve(
        self, *, subject: str, class_level: str, topic: str | None, query: str, k: int = 4
    ) -> list[RetrievedChunk]:
        self._reload_if_changed()
        scope_key = (norm_label(subject), norm_label(class_level))
        idx = self._topic_idx.get(scope_key + (norm_label(topic),)) if topic else None
        scope = "topic"
        if idx is None:
            idx = self._scope_idx.get(scope_key)
            scope = "subject"
        if idx is None or not idx.chunks:
            return []

        scores = idx.bm25.scores(tokenize(f"{topic or ''} {query}"))
        order = sorted(range(len(scores)), key=lambda i: (-scores[i], i))
        picks = [i for i in order if scores[i] > 0][:k]
        if not picks:
            if scope == "subject":
                return []  # never feed unrelated text as "curriculum"
            picks = list(range(min(k, len(idx.chunks))))  # topic opening, in page order
        return [RetrievedChunk(idx.chunks[i], scores[i], scope) for i in picks]
