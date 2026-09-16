"""
models/topic.py

"A topic must belong to a subject" (issue's own technical note) —
subject_id is required, not optional.
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    # Only seen by static type checkers (Pylance/mypy) - never runs.
    # SQLAlchemy still resolves "Subject" and "Lesson" below via its
    # own model registry at runtime, exactly as before; this import
    # exists purely so your editor knows what those forward-reference
    # strings point to and stops flagging them as undefined.
    from app.models.lesson import Lesson
    from app.models.subject import Subject


class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True)

    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False, index=True
    )

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    subject: Mapped["Subject"] = relationship(back_populates="topics")
    lessons: Mapped[list["Lesson"]] = relationship(
        back_populates="topic",
        cascade="all, delete-orphan",
        order_by="Lesson.order_index",
    )