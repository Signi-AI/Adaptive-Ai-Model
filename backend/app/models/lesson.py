from __future__ import annotations
import uuid 
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import UUID, DateTime, Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base  

if TYPE_CHECKING:
    from app.models.topic import Topic
    from app.models.learning_objective import LearningObjective


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )

    # Converted Foreign Key to UUID to match Topic.id
    topic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("topics.id", ondelete="CASCADE"),
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
    
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    sequence: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    estimated_learning_time: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
    )
    
    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
    
    # Modernized timestamp handling across models
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
    
    # Single, explicit relationship definition back to Topic
    topic: Mapped["Topic"] = relationship(
        "Topic",
        back_populates="lessons",
    )
    
    # Forward relationship pointing to LearningObjective
    learning_objectives: Mapped[List["LearningObjective"]] = relationship(
        "LearningObjective",
        back_populates="lesson",
        cascade="all, delete-orphan",
    )
