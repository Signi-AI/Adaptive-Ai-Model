"""
models/subject.py

Top of the content hierarchy. A Subject is shared curriculum data
(e.g. "Mathematics") — it does not belong to any one Student. This
issue's own technical notes only specify Topic -> Subject and
Lesson -> Topic ownership, so Subject stays standalone here.
"""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.topic import Topic


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
        )

    name: Mapped[str] = mapped_column(
        String(120), 
        nullable=False,
        index=True
        )


    code: Mapped[str | None] = mapped_column(
        String(20), 
        unique=True, 
        nullable=True,
        index=True
        )


    description: Mapped[str | None] = mapped_column(
        Text, 
        nullable=True,
        index=True
        )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        server_default=func.now(),
        nullable=False
    )

    topics: Mapped[list["Topic"]] = relationship(
        back_populates="subject", 
        cascade="all, delete-orphan"
    )
