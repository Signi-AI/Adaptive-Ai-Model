from __future__ import annotations
import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import UUID, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
 
if TYPE_CHECKING:
    from app.models.topic import Topic


class Subject(Base):
    __tablename__ = "subjects"

    # Primary key uses UUID (Perfect)
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

    # Standardized timezone-aware mapping across all schemas
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Forward relationship linking to Topic (Perfect configuration)
    topics: Mapped[List["Topic"]] = relationship(
        "Topic",
        back_populates="subject", 
        cascade="all, delete-orphan"
    )
