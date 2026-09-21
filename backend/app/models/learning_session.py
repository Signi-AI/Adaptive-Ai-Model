"""
models/learning_session.py

Tracks what a student was last doing - which subject, topic, and
(optionally) lesson they were on, and when. This is activity history,
not adaptive intelligence: no mastery, no scoring, no decisions about
what to teach next. One row per selection is enough to answer "what
did they do last session" and to let a frontend offer "continue where
you left off" - correctly, even across multiple in-progress topics,
since each selection is its own row rather than a single pointer that
gets overwritten the moment the student switches subjects.

lesson_id is nullable: a session starts the moment a topic is
selected, before any specific lesson has been opened.

ended_at exists but nothing sets it yet. There's no event anywhere in
the system today that marks a session "finished" - that's the AI
teaching session (unbuilt). Leave it null until that trigger exists;
don't guess at when a session "ends."
"""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.lesson import Lesson
    from app.models.subject import Subject
    from app.models.topic import Topic


class LearningSession(Base):
    __tablename__ = "learning_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)

    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
    )
    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id", ondelete="CASCADE"), nullable=False
    )
    lesson_id: Mapped[int | None] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"), nullable=True
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, index=True
    )
    # Reserved for a future issue - nothing sets this yet (see module docstring).
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    subject: Mapped["Subject"] = relationship()
    topic: Mapped["Topic"] = relationship()
    lesson: Mapped["Lesson | None"] = relationship()