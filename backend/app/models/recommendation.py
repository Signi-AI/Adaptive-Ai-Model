"""models/recommendation.py  (Issue 08)

A stored, structured learning recommendation: persistent learning memory, not
text that only lives inside an AI conversation.

* subject_id is stored (the issue lists it) but is always DERIVED from the topic
  at creation time, never taken from a caller.
* topic_id      the topic the student should study.
* related_topic_id  the topic whose adaptive decision triggered it, when that is
  a different topic (e.g. REVIEW of a prerequisite, or ADVANCE to the next topic).
* adaptive_decision_id  traceability back to the decision that produced it; also
  makes regenerating from the same decision a no-op.

At most ONE open (PENDING/ACTIVE) recommendation exists per (student, topic,
type): enforced by the partial unique index below, so concurrent requests can
never create duplicates. Closed ones (COMPLETED/DISMISSED/SUPERSEDED) stay as
learning history.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.curriculum_ids import SubjectId, TopicId, id_column_type
from app.core.database import Base
from app.core.learning_enums import (
    Difficulty,
    RecommendationPriority,
    RecommendationStatus,
    RecommendationType,
)

_OPEN = text("status IN ('PENDING', 'ACTIVE')")


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Recommendation(Base):
    __tablename__ = "recommendations"
    __table_args__ = (
        Index(
            "uq_recommendations_open_student_topic_type",
            "student_id",
            "topic_id",
            "type",
            unique=True,
            postgresql_where=_OPEN,
            sqlite_where=_OPEN,
        ),
        Index("ix_recommendations_student_status", "student_id", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    subject_id: Mapped[SubjectId] = mapped_column(
        id_column_type(), ForeignKey("subjects.id"), nullable=False, index=True
    )
    topic_id: Mapped[TopicId] = mapped_column(
        id_column_type(), ForeignKey("topics.id"), nullable=False, index=True
    )
    related_topic_id: Mapped[TopicId | None] = mapped_column(
        id_column_type(), ForeignKey("topics.id"), nullable=True
    )
    adaptive_decision_id: Mapped[int | None] = mapped_column(
        ForeignKey("adaptive_decisions.id", ondelete="SET NULL"), nullable=True
    )

    type: Mapped[RecommendationType] = mapped_column(
        SAEnum(RecommendationType, name="recommendation_type"), nullable=False
    )
    action: Mapped[str] = mapped_column(Text, nullable=False)       # what to do
    reason: Mapped[str] = mapped_column(Text, nullable=False)       # why
    reason_code: Mapped[str] = mapped_column(String(50), nullable=False)
    priority: Mapped[RecommendationPriority] = mapped_column(
        SAEnum(RecommendationPriority, name="recommendation_priority"), nullable=False
    )
    difficulty: Mapped[Difficulty | None] = mapped_column(
        SAEnum(Difficulty, name="recommendation_difficulty"), nullable=True
    )
    status: Mapped[RecommendationStatus] = mapped_column(
        SAEnum(RecommendationStatus, name="recommendation_status"),
        nullable=False,
        default=RecommendationStatus.PENDING,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False
    )
