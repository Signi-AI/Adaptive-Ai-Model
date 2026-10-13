"""models/lesson_completion.py  (Issue 06)

Records that a student finished a lesson. Progress ("lessons completed",
"topics studied") needs this and no existing table holds it. One row per
(student, lesson); completing twice is a no-op.

Written only through ProgressService.mark_lesson_completed(), which the
Learning Session flow calls when a lesson ends. There is deliberately no
public endpoint for it: students must not be able to mark their own progress.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.curriculum_ids import LessonId, id_column_type
from app.core.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class LessonCompletion(Base):
    __tablename__ = "lesson_completions"
    __table_args__ = (
        UniqueConstraint("student_id", "lesson_id", name="uq_lesson_completions_student_lesson"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    lesson_id: Mapped[LessonId] = mapped_column(
        id_column_type(), ForeignKey("lessons.id"), nullable=False, index=True
    )
    completed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_utcnow, nullable=False)