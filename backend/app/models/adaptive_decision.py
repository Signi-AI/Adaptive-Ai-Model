"""models/adaptive_decision.py  (Issue 07)

One row per adaptive decision that the learning flow chose to keep. Stored
because decisions are meaningful for learning history, debugging and later
analysis -- and because the engine reads the LAST decision to avoid loops
(REVISE -> teach -> REVISE ...) and to change difficulty one level at a time.

Intermediate calculations are not stored. Previews (persist=False) leave no row.
session_id is an opaque reference: the Learning Session table is owned by
another issue, so there is no FK yet.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.curriculum_ids import TopicId, id_column_type
from app.core.database import Base
from app.core.learning_enums import AdaptiveAction, Difficulty


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AdaptiveDecision(Base):
    __tablename__ = "adaptive_decisions"
    __table_args__ = (Index("ix_adaptive_decisions_student_topic", "student_id", "topic_id", "id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    topic_id: Mapped[TopicId] = mapped_column(id_column_type(), ForeignKey("topics.id"), nullable=False)
    session_id: Mapped[str | None] = mapped_column(String(64), nullable=True)

    action: Mapped[AdaptiveAction] = mapped_column(SAEnum(AdaptiveAction, name="adaptive_action"), nullable=False)
    difficulty: Mapped[Difficulty | None] = mapped_column(
        SAEnum(Difficulty, name="adaptive_difficulty"), nullable=True
    )
    reason_code: Mapped[str] = mapped_column(String(50), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)

    # Snapshot of the state the decision was based on.
    mastery_score: Mapped[float] = mapped_column(Float, nullable=False)
    recent_performance: Mapped[float] = mapped_column(Float, nullable=False)
    attempts_at_decision: Mapped[int] = mapped_column(Integer, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, nullable=False)