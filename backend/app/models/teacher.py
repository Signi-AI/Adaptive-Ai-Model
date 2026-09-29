"""
ORM models for the Teacher domain.

Three tables, nothing more (per the issue):
  - Teacher                  the human teacher's identity/profile
  - TeacherStudentAssignment which students a teacher may supervise
  - TeacherGuidance          human guidance, stored separately from any AI feedback

Student and Learning data are NOT duplicated here. Assignments and guidance
point at students.id; nothing else about a student lives in this module.
"""
import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, Text, func, text
from sqlalchemy import Enum as PgEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.student import Student  # noqa: F401  (makes the students table/class resolvable here)


class TeacherStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DEACTIVATED = "DEACTIVATED"


class AssignmentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ENDED = "ENDED"


class Teacher(Base):
    __tablename__ = "teachers"
    __table_args__ = (
        # Case-insensitive uniqueness on the login identifier, case preserved
        # for display (same approach as students.username).
        Index("ix_teachers_email_lower", text("lower(email)"), unique=True),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    phone_number: Mapped[str | None] = mapped_column(String(32), nullable=True)
    specialization: Mapped[str | None] = mapped_column(String(120), nullable=True)

    status: Mapped[TeacherStatus] = mapped_column(
        PgEnum(TeacherStatus, name="teacher_status"),
        nullable=False,
        default=TeacherStatus.ACTIVE,
        server_default=TeacherStatus.ACTIVE.value,
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

    assignments: Mapped[list["TeacherStudentAssignment"]] = relationship(
        back_populates="teacher", cascade="all, delete-orphan"
    )


class TeacherStudentAssignment(Base):
    """
    "Is student X assigned to teacher Y?" is answered by an ACTIVE row here.
    Ending an assignment flips status to ENDED (history is kept); the partial
    unique index allows a teacher/student pair to be re-assigned later.
    """
    __tablename__ = "teacher_student_assignments"
    __table_args__ = (
        Index(
            "uq_teacher_student_active_assignment",
            "teacher_id",
            "student_id",
            unique=True,
            postgresql_where=text("status = 'ACTIVE'"),
        ),
        Index("ix_teacher_student_assignments_teacher_id", "teacher_id"),
        Index("ix_teacher_student_assignments_student_id", "student_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[AssignmentStatus] = mapped_column(
        PgEnum(AssignmentStatus, name="assignment_status"),
        nullable=False,
        default=AssignmentStatus.ACTIVE,
        server_default=AssignmentStatus.ACTIVE.value,
    )
    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    teacher: Mapped["Teacher"] = relationship(back_populates="assignments")
    student: Mapped["Student"] = relationship()


class TeacherGuidance(Base):
    """
    Human teacher guidance. Deliberately its own table: AI-generated feedback
    is never stored here, and guidance is never stored with AI feedback.

    subject/topic are plain text and attempt_id is a plain UUID with no FK on
    purpose -- the curriculum and attempts tables belong to other domains and
    don't exist yet. When they do, tighten these to real foreign keys.
    """
    __tablename__ = "teacher_guidance"
    __table_args__ = (
        Index(
            "ix_teacher_guidance_student_teacher_created",
            "student_id",
            "teacher_id",
            "created_at",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    # RESTRICT: a teacher who has written guidance can be deactivated, but the
    # history of human intervention must not vanish because of a delete.
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("teachers.id", ondelete="RESTRICT"), nullable=False
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False
    )
    subject: Mapped[str | None] = mapped_column(String(120), nullable=True)
    topic: Mapped[str | None] = mapped_column(String(120), nullable=True)
    attempt_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), nullable=True)

    guidance_text: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default=text("false")
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    teacher: Mapped["Teacher"] = relationship()
