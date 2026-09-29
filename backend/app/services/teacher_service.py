"""
Business logic for the Teacher domain. Routes stay thin; the rule that governs
almost everything lives here: get_assigned_student(). Every student-scoped
operation goes through it, so a student_id from the client is never trusted
on its own.
"""
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.core.teacher_security import create_teacher_access_token
from app.models.student import Student
from app.models.teacher import (
    AssignmentStatus,
    Teacher,
    TeacherGuidance,
    TeacherStatus,
    TeacherStudentAssignment,
)
from app.schemas.teacher import (
    AssignedStudentSummary,
    AttemptDetail,
    AttemptSummary,
    GuidanceCreate,
    GuidancePublic,
    StudentOverview,
    StudentProfileForTeacher,
    StudentProgressReport,
    TeacherUpdate,
)
from app.services import teacher_learning_adapter


# --------------------------------------------------------------------------
# Authentication
# --------------------------------------------------------------------------

def authenticate_teacher(db: Session, email: str, password: str, device_label=None) -> tuple[Teacher, str, datetime]:
    """
    Returns (teacher, access_token, expires_at). Same 401 for "unknown email"
    and "wrong password" so the endpoint can't be used to enumerate teachers.
    """
    invalid = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password"
    )

    teacher = db.execute(
        select(Teacher).where(func.lower(Teacher.email) == email.strip().lower())
    ).scalar_one_or_none()
    if teacher is None:
        raise invalid
    if not verify_password(password, teacher.password_hash):
        raise invalid
    if teacher.status != TeacherStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="This account is not active"
        )

    teacher.last_login_at = datetime.now(timezone.utc)
    db.commit()

    token, expires_at = create_teacher_access_token(str(teacher.id))
    return teacher,token, expires_at


# --------------------------------------------------------------------------
# Account creation (internal -- there is deliberately NO public route for this;
# used by the dev seed script and tests)
# --------------------------------------------------------------------------

def create_teacher(
    db: Session,
    *,
    email: str,
    full_name: str,
    password: str,
    phone_number: str | None = None,
    specialization: str | None = None,
) -> Teacher:
    teacher = Teacher(
        email=email.strip(),
        full_name=full_name.strip(),
        password_hash=hash_password(password),
        phone_number=phone_number,
        specialization=specialization,
        status=TeacherStatus.ACTIVE,
    )
    db.add(teacher)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="A teacher with that email already exists"
        )
    db.refresh(teacher)
    return teacher


# --------------------------------------------------------------------------
# Profile
# --------------------------------------------------------------------------

def update_profile(db: Session, teacher: Teacher, data: TeacherUpdate) -> Teacher:
    # TeacherUpdate only contains editable fields, so there is nothing here a
    # client could use to touch email/status/id, and `teacher` always comes
    # from the token -- never from a client-supplied id.
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(teacher, field, value)
    db.commit()
    db.refresh(teacher)
    return teacher


# --------------------------------------------------------------------------
# Teacher <-> Student assignment
# --------------------------------------------------------------------------

def assign_student_to_teacher(
    db: Session, teacher_id: uuid.UUID, student_id: uuid.UUID
) -> TeacherStudentAssignment:
    """Internal (no public route in this issue). Idempotent for an active pair."""
    if db.get(Teacher, teacher_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    if db.get(Student, student_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    existing = db.execute(
        select(TeacherStudentAssignment).where(
            TeacherStudentAssignment.teacher_id == teacher_id,
            TeacherStudentAssignment.student_id == student_id,
            TeacherStudentAssignment.status == AssignmentStatus.ACTIVE,
        )
    ).scalar_one_or_none()
    if existing is not None:
        return existing

    assignment = TeacherStudentAssignment(teacher_id=teacher_id, student_id=student_id)
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment


def end_assignment(db: Session, teacher_id: uuid.UUID, student_id: uuid.UUID) -> None:
    assignment = db.execute(
        select(TeacherStudentAssignment).where(
            TeacherStudentAssignment.teacher_id == teacher_id,
            TeacherStudentAssignment.student_id == student_id,
            TeacherStudentAssignment.status == AssignmentStatus.ACTIVE,
        )
    ).scalar_one_or_none()
    if assignment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assignment not found")
    assignment.status = AssignmentStatus.ENDED
    assignment.ended_at = datetime.now(timezone.utc)
    db.commit()


def get_assigned_student(db: Session, teacher_id: uuid.UUID, student_id: uuid.UUID) -> Student:
    """
    THE authorization check. Returns the student only if an ACTIVE assignment
    links them to this teacher. "No such student" and "student belongs to
    another teacher" produce the identical 404, so probing student ids reveals
    nothing (this is the IDOR defence).
    """
    student = db.execute(
        select(Student)
        .join(TeacherStudentAssignment, TeacherStudentAssignment.student_id == Student.id)
        .where(
            TeacherStudentAssignment.teacher_id == teacher_id,
            TeacherStudentAssignment.student_id == student_id,
            TeacherStudentAssignment.status == AssignmentStatus.ACTIVE,
        )
    ).scalar_one_or_none()
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found among your assigned students",
        )
    return student


# --------------------------------------------------------------------------
# Student monitoring
# --------------------------------------------------------------------------

def list_assigned_students(db: Session, teacher: Teacher) -> list[AssignedStudentSummary]:
    rows = db.execute(
        select(Student, TeacherStudentAssignment.assigned_at)
        .join(TeacherStudentAssignment, TeacherStudentAssignment.student_id == Student.id)
        .where(
            TeacherStudentAssignment.teacher_id == teacher.id,
            TeacherStudentAssignment.status == AssignmentStatus.ACTIVE,
        )
        .order_by(func.lower(Student.full_name))
    ).all()

    summaries = []
    for student, assigned_at in rows:
        progress = teacher_learning_adapter.get_student_progress(db, student.id)
        summaries.append(
            AssignedStudentSummary(
                student_id=student.id,
                full_name=student.full_name,
                class_level=student.class_level,
                overall_progress=progress.overall_progress,
                last_activity_at=student.last_login_at,
                assigned_at=assigned_at,
            )
        )
    return summaries


def get_student_overview(db: Session, teacher: Teacher, student_id: uuid.UUID) -> StudentOverview:
    student = get_assigned_student(db, teacher.id, student_id)
    return StudentOverview(
        profile=StudentProfileForTeacher.model_validate(student),
        progress=teacher_learning_adapter.get_student_progress(db, student.id),
        recent_attempts=teacher_learning_adapter.list_student_attempts(
            db, student.id, limit=5, offset=0
        ),
        recent_guidance=[
            GuidancePublic.model_validate(g)
            for g in _query_guidance(db, teacher.id, student.id, limit=5, offset=0)
        ],
    )


def get_student_progress(
    db: Session, teacher: Teacher, student_id: uuid.UUID
) -> StudentProgressReport:
    student = get_assigned_student(db, teacher.id, student_id)
    return teacher_learning_adapter.get_student_progress(db, student.id)


def list_student_attempts(
    db: Session, teacher: Teacher, student_id: uuid.UUID, *, limit: int, offset: int
) -> list[AttemptSummary]:
    student = get_assigned_student(db, teacher.id, student_id)
    return teacher_learning_adapter.list_student_attempts(
        db, student.id, limit=limit, offset=offset
    )


def get_student_attempt(
    db: Session, teacher: Teacher, student_id: uuid.UUID, attempt_id: uuid.UUID
) -> AttemptDetail:
    student = get_assigned_student(db, teacher.id, student_id)
    attempt = teacher_learning_adapter.get_student_attempt(db, student.id, attempt_id)
    if attempt is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found")
    return attempt


# --------------------------------------------------------------------------
# Human guidance
# --------------------------------------------------------------------------

def _query_guidance(
    db: Session, teacher_id: uuid.UUID, student_id: uuid.UUID, *, limit: int, offset: int
) -> list[TeacherGuidance]:
    # A teacher only ever sees guidance THEY wrote -- never another teacher's,
    # even for a student both happen to supervise.
    result = db.execute(
        select(TeacherGuidance)
        .where(
            TeacherGuidance.teacher_id == teacher_id,
            TeacherGuidance.student_id == student_id,
        )
        .order_by(TeacherGuidance.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    return list(result.scalars().all())


def create_guidance(
    db: Session, teacher: Teacher, student_id: uuid.UUID, data: GuidanceCreate
) -> TeacherGuidance:
    student = get_assigned_student(db, teacher.id, student_id)

    subject, topic = data.subject, data.topic
    if data.attempt_id is not None:
        attempt = teacher_learning_adapter.get_student_attempt(db, student.id, data.attempt_id)
        if attempt is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Attempt not found for this student"
            )
        subject = subject or attempt.subject
        topic = topic or attempt.topic

    guidance = TeacherGuidance(
        teacher_id=teacher.id,  # always from the token, never from the request body
        student_id=student.id,
        subject=subject,
        topic=topic,
        attempt_id=data.attempt_id,
        guidance_text=data.guidance_text,
    )
    db.add(guidance)
    try:
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        # Internal database errors are never passed through to the client.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Could not save guidance"
        )
    db.refresh(guidance)
    return guidance


def list_guidance(
    db: Session, teacher: Teacher, student_id: uuid.UUID, *, limit: int, offset: int
) -> list[TeacherGuidance]:
    student = get_assigned_student(db, teacher.id, student_id)
    return _query_guidance(db, teacher.id, student.id, limit=limit, offset=offset)
