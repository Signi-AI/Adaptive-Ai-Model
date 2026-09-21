"""
models/learning_session.py

Tracks what a student was last doing - which topic they selected and
when. This is activity history, not adaptive intelligence: no
mastery, no scoring, no decisions about what to teach next. One row
per topic selection is enough to answer "what did they do last
session" and to let a frontend offer "continue where you left off."

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

    started_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False, index=True
    )
    # Reserved for a future issue - nothing sets this yet (see module docstring).
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    subject: Mapped["Subject"] = relationship()
    topic: Mapped["Topic"] = relationship()