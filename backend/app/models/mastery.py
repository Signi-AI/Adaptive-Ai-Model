"""Mastery storage: one row per student + topic. No formulas here."""
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, UniqueConstraint

from app.database import Base


def _utcnow():
    return datetime.now(timezone.utc)


class Mastery(Base):
    __tablename__ = "mastery"
    # Mastery is per student per topic, never global
    __table_args__ = (
        UniqueConstraint("student_id", "topic_id", name="uq_mastery_student_topic"),
    )

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False, index=True)
    mastery = Column(Float, nullable=False)  # current value (0-1)
    previous_mastery = Column(Float, nullable=True)  # value before the last answer
    updated_at = Column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False
    )

    def apply_update(self, previous: float, new: float) -> None:
        # Store the values from BKTResult (previous and new)
        self.previous_mastery = previous
        self.mastery = new