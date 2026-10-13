"""
What's left of the Teacher domain's own tables once identity moved to
app/models/user.py: the relationship between a teacher and the students they
supervise, and the guidance they write. Both teacher_id and student_id below
point at the SAME users table -- which row is which is determined by that
row's role at the time the relationship/guidance was created, not by which
table it lives in (there's only one table now).

If a teacher is demoted back to a student (see services/user_service.py::
demote_to_student), every TeacherStudentAssignment and TeacherGuidance row
where they were the teacher_id is deleted as part of "erase and start over"
-- rows referencing them as a student are unaffected by that, since they
have none until they've actually been a student again.
"""
import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, Text, func, text
from sqlalchemy import Enum as PgEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.user import User  # noqa: F401  (makes the users table/class resolvable here)


class AssignmentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ENDED = "ENDED"


class TeacherStudentAssignment(Base):
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
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
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

    teacher: Mapped["User"] = relationship(foreign_keys=[teacher_id])
    student: Mapped["User"] = relationship(foreign_keys=[student_id])


class TeacherGuidance(Base):
    """
    Human teacher guidance. Its own table on purpose: AI-generated feedback
    is never stored here, and guidance is never stored with AI feedback.
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
    teacher_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
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

    teacher: Mapped["User"] = relationship(foreign_keys=[teacher_id])
