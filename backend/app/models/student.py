"""
ORM models for the Student domain.

Every other domain in TOALM refers to a learner via Student.id — this is
the stable identity the whole system hangs off of (per the issue's
"Dependencies" section). Nothing outside this module should implement
its own notion of student identity or authentication.
"""
import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, text
from sqlalchemy import Enum as PgEnum
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ClassLevel(str, Enum):
    """
    Tanzania's education levels, in order. Fixed on purpose — not free
    text — so the curriculum domain can reliably filter subjects and
    topics by level later, and so a student's progress can be compared
    meaningfully against peers in the same class.
    """
    STD_1 = "STD_1"
    STD_2 = "STD_2"
    STD_3 = "STD_3"
    STD_4 = "STD_4"
    STD_5 = "STD_5"
    STD_6 = "STD_6"
    STD_7 = "STD_7"
    FORM_1 = "FORM_1"
    FORM_2 = "FORM_2"
    FORM_3 = "FORM_3"
    FORM_4 = "FORM_4"
    FORM_5 = "FORM_5"
    FORM_6 = "FORM_6"
    UNIVERSITY="DIPLOMA"
    UNIVERSIT="BACHELOR"


class StudentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DEACTIVATED = "DEACTIVATED"


class Student(Base):
    __tablename__ = "students"
    __table_args__ = (
        # Case is preserved for display, but uniqueness is enforced on
        # the lowercased value — "Amina" and "amina" can't become two
        # separate accounts. A plain unique=True on the column would be
        # both redundant with this (it's a strict subset of what this
        # index already guarantees) and, worse, would let create_all()
        # (used by the test suite) produce a schema that silently
        # diverges from what the Alembic migration actually creates.
        Index("ix_students_username_lower", text("lower(username)"), unique=True),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String(32), nullable=False)

    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    class_level: Mapped[ClassLevel] = mapped_column(
        PgEnum(ClassLevel, name="class_level"), nullable=False
    )
    status: Mapped[StudentStatus] = mapped_column(
        PgEnum(StudentStatus, name="student_status"),
        nullable=False,
        default=StudentStatus.ACTIVE,
        server_default=StudentStatus.ACTIVE.value,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    sessions: Mapped[list["StudentSession"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )


class StudentSession(Base):
    """
    One row per *login*, not per physical device. Lab machines are
    shared between students, so hardware fingerprinting would be both
    unreliable and the wrong model — what actually needs tracking is
    each login instance (tied to a refresh token) so it can be listed
    and revoked independently of the machine it happened on.
    """
    __tablename__ = "student_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )

    # Optional, user-supplied label for the student's own "Sessions"
    # list (e.g. "Lab PC 3"). Purely informational — never used for any
    # security decision.
    device_label: Mapped[str | None] = mapped_column(String(255), nullable=True)

    refresh_token_hash: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    revoked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    student: Mapped["Student"] = relationship(back_populates="sessions")
