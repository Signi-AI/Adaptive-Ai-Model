"""models/mastery.py  (Issue 06)

Mastery = how well ONE student currently understands ONE learning area.

Granularity
-----------
* A topic-level row (learning_objective_id IS NULL) exists for every
  (student, topic) that has evidence. It is updated by EVERY attempt on the
  topic and is the level the Artificial Teacher / adaptive engine read.
* An objective-level row additionally exists when an attempt names a learning
  objective. Objectives hang off lessons (LearningObjective.lesson_id), so the
  topic is always derived via the lesson, never trusted from the caller.

Subject is intentionally NOT stored here: it is always topic.subject_id, and a
second copy could only drift out of sync.

Status, strength and weakness
-----------------------------
`status` is persisted (cheap to filter on) and recomputed on every update, so
it can move down as well as up. Strength / weakness are DERIVED on read from
score + attempts (see services/mastery_rules.py) and are never stored.

MasteryHistory
--------------
Append-only ledger: one row per attempt that changed a mastery row. It keeps
the student's learning history instead of only the latest result, supplies the
"recent performance" window, and its unique (mastery_id, attempt_ref) pair
makes reprocessing the same attempt a no-op (no double counting).
attempt_ref is deliberately an opaque string: the Attempt table is owned by
another issue, so there is no FK yet.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    text,
)
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.core.learning_enums import MasteryStatus

__all__ = ["Mastery", "MasteryHistory", "MasteryStatus"]


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Mastery(Base):
    __tablename__ = "masteries"
    __table_args__ = (
        # One topic-level row and one row per objective, per student.
        # (A plain UNIQUE over a nullable column would allow duplicate NULLs.)
        Index(
            "uq_masteries_student_topic",
            "student_id",
            "topic_id",
            unique=True,
            postgresql_where=text("learning_objective_id IS NULL"),
            sqlite_where=text("learning_objective_id IS NULL"),
        ),
        Index(
            "uq_masteries_student_objective",
            "student_id",
            "learning_objective_id",
            unique=True,
            postgresql_where=text("learning_objective_id IS NOT NULL"),
            sqlite_where=text("learning_objective_id IS NOT NULL"),
        ),
        CheckConstraint("mastery_score >= 0 AND mastery_score <= 1", name="ck_masteries_score_range"),
        CheckConstraint("attempts_considered >= 0", name="ck_masteries_attempts_nonneg"),
        CheckConstraint(
            "correct_attempts >= 0 AND correct_attempts <= attempts_considered",
            name="ck_masteries_correct_range",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"), nullable=False, index=True)
    learning_objective_id: Mapped[int | None] = mapped_column(
        ForeignKey("learning_objectives.id"), nullable=True, index=True
    )

    mastery_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    attempts_considered: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    correct_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[MasteryStatus] = mapped_column(
        SAEnum(MasteryStatus, name="mastery_status"),
        nullable=False,
        default=MasteryStatus.BEGINNING,
    )

    last_assessed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False
    )

    @property
    def incorrect_attempts(self) -> int:
        return self.attempts_considered - self.correct_attempts


class MasteryHistory(Base):
    __tablename__ = "mastery_history"
    __table_args__ = (
        UniqueConstraint("mastery_id", "attempt_ref", name="uq_mastery_history_mastery_attempt"),
        Index("ix_mastery_history_mastery_id_id", "mastery_id", "id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    mastery_id: Mapped[int] = mapped_column(
        ForeignKey("masteries.id", ondelete="CASCADE"), nullable=False
    )
    attempt_ref: Mapped[str] = mapped_column(String(64), nullable=False)

    outcome: Mapped[float] = mapped_column(Float, nullable=False)        # 0..1 score of the attempt
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)     # 1..5
    score_before: Mapped[float] = mapped_column(Float, nullable=False)
    score_after: Mapped[float] = mapped_column(Float, nullable=False)

    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, nullable=False)