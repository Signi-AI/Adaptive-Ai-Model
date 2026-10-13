"""models/attempt.py

Tracks individual student question attempts.

Role in the architecture:
-------------------------
1. Atomic Event Record:
   Captures the exact student interaction with an assessment or practice question.
   Historical attempts are immutable once recorded.

2. Evidence Source for Mastery:
   When an attempt completes, its score, difficulty, and curriculum targets
   are passed to `MasteryService.record_attempt()` via `AttemptEvidence`
   to update topic- and objective-level mastery.

3. Teacher Supervision & Guidance:
   Supplies `AttemptSummary` and `AttemptDetail` to the Teacher domain
   (e.g. for student progress reviews, diagnosing misconceptions, and linking
   human feedback via `TeacherGuidance.attempt_id`).

4. Snapshot of Historical Context:
   Stores the rendered `question_text`, `student_answer`, and `expected_answer`
   at the time of the attempt so that template edits, deletions, or algorithm
   changes never invalidate historical attempt records.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.curriculum_ids import id_column_type
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.generated_question import GeneratedQuestion
    from app.models.learning_objective import LearningObjective
    from app.models.learning_session import LearningSession
    from app.models.lesson import Lesson
    from app.models.subject import Subject
    from app.models.topic import Topic
    from app.models.user import User
    from app.schemas.mastery import AttemptEvidence
    from app.schemas.teacher import AttemptDetail, AttemptSummary

__all__ = ["Attempt"]


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Attempt(Base):
    __tablename__ = "attempts"
    __table_args__ = (
        CheckConstraint("score >= 0.0 AND score <= 1.0", name="ck_attempts_score_range"),
        CheckConstraint("difficulty >= 1 AND difficulty <= 5", name="ck_attempts_difficulty_range"),
        Index("ix_attempts_student_attempted", "student_id", "attempted_at"),
        Index("ix_attempts_student_topic_attempted", "student_id", "topic_id", "attempted_at"),
    )

    # Primary key — UUID matching teacher guidance and schema requirements
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Student reference
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Curriculum references (using unified UUID id_column_type)
    subject_id: Mapped[uuid.UUID] = mapped_column(
        id_column_type(),
        ForeignKey("subjects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    topic_id: Mapped[uuid.UUID] = mapped_column(
        id_column_type(),
        ForeignKey("topics.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    lesson_id: Mapped[uuid.UUID | None] = mapped_column(
        id_column_type(),
        ForeignKey("lessons.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    learning_objective_id: Mapped[uuid.UUID | None] = mapped_column(
        id_column_type(),
        ForeignKey("learning_objectives.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Optional origin question and session
    question_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("generated_questions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    session_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("learning_sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Content snapshot — preserves context even if templates/questions are modified
    question_text: Mapped[str] = mapped_column(Text, nullable=False)
    student_answer: Mapped[str] = mapped_column(Text, nullable=False)
    expected_answer: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Evaluation results
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    result: Mapped[str] = mapped_column(String(32), nullable=False, default="INCORRECT")

    # Difficulty (1..5 scale aligned with mastery_rules)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False, default=3)

    # System/AI feedback & pedagogical explanation
    ai_feedback: Mapped[str | None] = mapped_column(Text, nullable=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Performance analytics
    time_spent_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Timestamps
    attempted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )

    # Relationships
    student: Mapped["User"] = relationship("User", foreign_keys=[student_id])
    subject: Mapped["Subject"] = relationship("Subject", foreign_keys=[subject_id])
    topic: Mapped["Topic"] = relationship("Topic", foreign_keys=[topic_id])
    lesson: Mapped["Lesson | None"] = relationship("Lesson", foreign_keys=[lesson_id])
    learning_objective: Mapped["LearningObjective | None"] = relationship(
        "LearningObjective", foreign_keys=[learning_objective_id]
    )
    question: Mapped["GeneratedQuestion | None"] = relationship(
        "GeneratedQuestion", foreign_keys=[question_id]
    )
    session: Mapped["LearningSession | None"] = relationship(
        "LearningSession", foreign_keys=[session_id]
    )

    # Property alias for teacher schemas compatibility
    @property
    def question(self) -> str:
        """Alias returning the question text as expected by AttemptDetail."""
        return self.question_text

    # Domain conversion helpers
    def to_evidence(self) -> AttemptEvidence:
        """Convert this attempt into the AttemptEvidence payload required by MasteryService."""
        from app.schemas.mastery import AttemptEvidence

        return AttemptEvidence(
            student_id=self.student_id,
            attempt_id=self.id,
            score=self.score,
            is_correct=self.is_correct,
            topic_id=self.topic_id,
            learning_objective_id=self.learning_objective_id,
            difficulty=self.difficulty,
            attempted_at=self.attempted_at or _utcnow(),
        )

    def to_summary(self) -> AttemptSummary:
        """Convert to AttemptSummary schema for teacher/student overview listings."""
        from app.schemas.teacher import AttemptSummary

        return AttemptSummary(
            id=self.id,
            subject=self.subject.name if self.subject else None,
            topic=self.topic.name if self.topic else None,
            result=self.result,
            score=self.score,
            attempted_at=self.attempted_at or _utcnow(),
        )

    def to_detail(self) -> AttemptDetail:
        """Convert to AttemptDetail schema for detailed teacher review."""
        from app.schemas.teacher import AttemptDetail

        return AttemptDetail(
            id=self.id,
            subject=self.subject.name if self.subject else None,
            topic=self.topic.name if self.topic else None,
            result=self.result,
            score=self.score,
            attempted_at=self.attempted_at or _utcnow(),
            question=self.question_text,
            student_answer=self.student_answer,
            expected_answer=self.expected_answer,
            ai_feedback=self.ai_feedback,
            session_id=self.session_id,
        )
