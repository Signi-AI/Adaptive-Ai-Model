"""
models/lesson.py

"A lesson must belong to a topic" (issue's own technical note) —
topic_id is required, not optional.

order_index is a deliberate, minimal addition beyond what the issue
literally asked for: a plain integer teaching-order hint within a
topic (1, 2, 3, ...). It is NOT a prerequisite graph — the issue
explicitly says not to build those in Week 1 — it's the minimum
needed for "give the system something meaningful to teach" (lessons
have to play in *some* order). Drop it if you'd rather defer ordering
entirely to a later issue.
"""

from datetime import datetime

from sqlalchemy import DateTime, Boolean,ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.topic import Topic


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        )

    topic_id: Mapped[int] = mapped_column(
        ForeignKey("topics.id"),
        nullable=False,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        )
    
    description: Mapped[str| None] = mapped_column(
        Text,
        nullable=True,
    )

    sequence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    estimated_learning_time: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    
    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utctimetuple,
        onupdate=datetime.utctimetuple,
        nullable=False,
    )
    
    topic = relationship(
        "Topic",
        back_populates="lesson",
    )
    
    learning_objectives = relationship(
        "LearningObjective",
        back_populates= "lesson",
        cascade="all, delete-orphan",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=func.now(), 
        nullable=False,
    )

    topic: Mapped["Topic"] = relationship(
        back_populates="lessons",
        )
