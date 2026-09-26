"""
Business logic for the Student domain. Routes stay thin (see
api/routes/auth.py and api/routes/students.py) — this module is where
registration, login, refresh, and profile rules actually live.
"""
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    generate_refresh_token,
    hash_password,
    hash_refresh_token,
    refresh_token_expiry,
    verify_password,
)
from app.models.student import Student, StudentSession, StudentStatus
from app.schemas.student import RegisterRequest, StudentUpdate


def register_student(db: Session, data: RegisterRequest) -> Student:
    existing = db.execute(select(Student).where(func.lower(Student.username) == data.username.lower()))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="That username is already taken",
        )

    student = Student(
        username=data.username,
        full_name=data.full_name,
        password_hash=hash_password(data.password),
        class_level=data.class_level,
        status=StudentStatus.ACTIVE,
    )
    db.add(student)
    try:
        db.commit()
    except IntegrityError:
        # Guards the small race window between the check above and the
        # insert (two registrations for the same username landing at once).
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="That username is already taken",
        )
    db.refresh(student)
    return student


def _get_student_by_username(db: Session, username: str) -> Student | None:
    result = db.execute(select(Student).where(func.lower(Student.username) == username.lower()))
    return result.scalar_one_or_none()


def authenticate_and_create_session(
    db: Session, username: str, password: str, device_label: str | None
) -> tuple[Student, StudentSession, str, str, datetime]:
    """
    Returns (student, session, access_token, raw_refresh_token, access_expires_at).

    Raises HTTP 401 with the SAME message for "unknown username" and
    "wrong password" on purpose — a caller must not be able to tell the
    two apart, or the endpoint becomes a way to enumerate valid usernames.
    """
    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password"
    )

    student = _get_student_by_username(db, username)
    if student is None:
        raise invalid_credentials

    if not verify_password(password, student.password_hash):
        raise invalid_credentials

    if student.status != StudentStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="This account is not active"
        )

    raw_refresh_token = generate_refresh_token()
    session = StudentSession(
        student_id=student.id,
        device_label=device_label,
        refresh_token_hash=hash_refresh_token(raw_refresh_token),
        expires_at=refresh_token_expiry(),
    )
    db.add(session)
    student.last_login_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(session)

    access_token, expires_at = create_access_token(
        student_id=str(student.id), session_id=str(session.id)
    )
    return student, session, access_token, raw_refresh_token, expires_at


def refresh_session(db: Session, raw_refresh_token: str) -> tuple[str, str, datetime]:
    """
    Validates and rotates a refresh token.
    Returns (new_access_token, new_raw_refresh_token, access_expires_at).
    """
    invalid_token = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token"
    )

    token_hash = hash_refresh_token(raw_refresh_token)
    result = db.execute(select(StudentSession).where(StudentSession.refresh_token_hash == token_hash))
    session = result.scalar_one_or_none()

    if session is None or session.revoked:
        raise invalid_token

    now = datetime.now(timezone.utc)
    if session.expires_at.replace(tzinfo=timezone.utc) < now:
        raise invalid_token

    # Rotate: the presented refresh token is dead the instant it's used,
    # so a stolen-and-replayed copy fails the moment the real one is used.
    new_raw_refresh_token = generate_refresh_token()
    session.refresh_token_hash = hash_refresh_token(new_raw_refresh_token)
    session.expires_at = refresh_token_expiry()
    session.last_activity_at = now

    db.commit()

    access_token, expires_at = create_access_token(
        student_id=str(session.student_id), session_id=str(session.id)
    )
    return access_token, new_raw_refresh_token, expires_at


def revoke_session(db: Session, student_id: uuid.UUID, session_id: uuid.UUID) -> None:
    result = db.execute(select(StudentSession).where(StudentSession.id == session_id))
    session = result.scalar_one_or_none()

    if session is None or session.student_id != student_id:
        # Same 404 whether the session doesn't exist or belongs to
        # someone else — this is what defeats the ID-manipulation attack
        # the issue calls out: probing other students' session IDs
        # teaches an attacker nothing from the response.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")

    session.revoked = True
    session.revoked_at = datetime.now(timezone.utc)
    db.commit()


def list_sessions(db: Session, student_id: uuid.UUID) -> list[StudentSession]:
    result = db.execute(
        select(StudentSession)
        .where(StudentSession.student_id == student_id)
        .order_by(StudentSession.last_activity_at.desc())
    )
    return list(result.scalars().all())


def update_profile(db: Session, student: Student, data: StudentUpdate) -> Student:
    if data.full_name is not None:
        student.full_name = data.full_name
    if data.class_level is not None:
        student.class_level = data.class_level
    db.commit()
    db.refresh(student)
    return student
