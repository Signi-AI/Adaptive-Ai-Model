from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class AcademicLevel(Base):
    __tablename__ = "academic_levels"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True,
        index=True
        )

    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    code: Mapped[str | None] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
        index=True,
    )

    Academic_Level_id: Mapped[str | None] = mapped_column(
        String(50),
        ForeignKey("academic_levels.id"),
        nullable=False,
        index=True,
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utctimetuple,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utctimetuple,
        onupdate=datetime.utctimetuple,
        nullable=False,
    )

    Academic_Level = relationship(
        "AcademicLevel",
        back_populates="subjects",
    )

    topics = relationship(
        "Topic",
        back_populates="subject",
        cascade="all, delete-orphan",
    )