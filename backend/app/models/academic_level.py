from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.subject import Subject
    from app.models.topic import Topic


class AcademicLevel(Base):
    __tablename__ = "academic_levels"

    # Primary Key converted to UUID
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    code: Mapped[Optional[str]] = mapped_column(
        String(20),
        unique=True,
        nullable=True,  # Changed to True because Mapped[str | None] allows null values
        index=True,
    )

    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        index=True,
    )

    # Foreign Key converted to UUID to perfectly match the primary key 'id'
    Academic_Level_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("academic_levels.id"),
        nullable=True,  # Self-referential parents must be nullable, otherwise you can't insert the first root level
        index=True,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # Fixed time stamp formatting to use native timezone-aware utcnow calls
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

    # Self-referential relationships configured explicitly
    parent_level: Mapped[Optional["AcademicLevel"]] = relationship(
        "AcademicLevel",
        remote_side=[id],
        back_populates="child_levels"
    )

    child_levels: Mapped[List["AcademicLevel"]] = relationship(
        "AcademicLevel",
        back_populates="parent_level"
    )

    subjects: Mapped[List["Subject"]] = relationship(
        "Subject",
        back_populates="academic_level",
        cascade="all, delete-orphan",
    )

    # Child relationships pointing to other separate models
    topics: Mapped[List["Topic"]] = relationship(
        "Topic",
        back_populates="academic_level",  # Make sure Topic model has: academic_level = relationship("AcademicLevel", back_populates="topics")
        cascade="all, delete-orphan",
    )
