from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.models.academic_level import AcademicLevel
    from app.models.lesson import Lesson
    from app.models.subject import Subject 
    from app.models.question_template import QuestionTemplate



class Topic(Base):
    __tablename__ = "topics"

    # Primary Key converted to UUID
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    # Added Foreign Key to AcademicLevel (UUID) to handle the relationship from the previous step
    academic_level_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("academic_levels.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Converted Subject Foreign Key to UUID (assuming Subjects table also uses UUIDs now)
    subject_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("subjects.id"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        index=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
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

    # Updated datetime formatting to be timezone-aware (safeguards against deprecation errors)
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

    # Relationship back to AcademicLevel
    academic_level: Mapped["AcademicLevel"] = relationship(
        "AcademicLevel",
        back_populates="topics",
    )

    # Relationship back to Subject
    subject: Mapped["Subject"] = relationship(
        "Subject",
        back_populates="topics",
    )

    # Relationship forward to Lessons
    lessons: Mapped[List["Lesson"]] = relationship(
        "Lesson",
        back_populates="topic",
        cascade="all, delete-orphan",
    )

        # Add this to map the reverse relationship from QuestionTemplate
    question_templates: Mapped[List["QuestionTemplate"]] = relationship(
        "QuestionTemplate",
        back_populates="topic",
        cascade="all, delete-orphan"
    )

