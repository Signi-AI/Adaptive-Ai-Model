from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.lesson import Lesson
    from app.models.question_template import QuestionTemplate


class LearningObjective(Base):
    __tablename__ = "learning_objectives"

    # Converted Primary Key to UUID to resolve typing conflicts
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    # Converted Foreign Key to UUID to match Lesson.id perfectly
    lesson_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    sequence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Modernized timestamp handling to use timezone-aware utcnow calls
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Clean relationship back to Lesson
    lesson = relationship(
        "Lesson",
        back_populates="learning_objectives",
    )

    # Added the missing relationship to satisfy QuestionTemplate's back_populates
    question_templates: Mapped[List["QuestionTemplate"]] = relationship(
        "QuestionTemplate",
        back_populates="learning_objective",
        cascade="all, delete-orphan",
    )
