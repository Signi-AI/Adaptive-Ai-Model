from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import UUID, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.academic_level import AcademicLevel
    from app.models.topic import Topic
    from app.models.question_template import QuestionTemplate


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(120), 
        nullable=False,
        index=True
    )

    code: Mapped[Optional[str]] = mapped_column(
        String(20), 
        unique=True, 
        nullable=True,
        index=True
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text, 
        nullable=True,
        index=True
    )

    academic_level_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("academic_levels.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    active: Mapped[bool] = mapped_column(default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    
    topics: Mapped[List["Topic"]] = relationship(
        "Topic",
        back_populates="subject", 
        cascade="all, delete-orphan"
    )

    academic_level: Mapped["AcademicLevel"] = relationship(
        "AcademicLevel",
        back_populates="subjects",
    )


    
    question_templates: Mapped[List["QuestionTemplate"]] = relationship(
        "QuestionTemplate",
        back_populates="subject",
        cascade="all, delete-orphan"
    )

