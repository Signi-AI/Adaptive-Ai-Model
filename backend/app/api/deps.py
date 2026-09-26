"""
Shared FastAPI dependencies: DB session + current-authenticated-student.

Every other domain in TOALM that needs to know "which student is this?"
should depend on get_current_student rather than re-implementing token
parsing — the issue is explicit that other domains must not build their
own authentication.
"""
import uuid
from collections.abc import Generator

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import decode_access_token
from app.models.student import Student, StudentSession, StudentStatus

_bearer_scheme = HTTPBearer(auto_error=True)

_credentials_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_student(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
    db: Session = Depends(get_db),
) -> Student:
    try:
        payload = decode_access_token(credentials.credentials)
        student_id = uuid.UUID(payload["sub"])
        session_id = uuid.UUID(payload["session_id"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise _credentials_error

    # The session is looked up on every request, not just the JWT
    # signature checked. This is what lets a logout on a shared lab PC
    # take effect immediately instead of waiting for the access token
    # (up to ACCESS_TOKEN_EXPIRE_MINUTES) to expire on its own.
    session_result = db.execute(select(StudentSession).where(StudentSession.id == session_id))
    session_row = session_result.scalar_one_or_none()
    if session_row is None or session_row.revoked:
        raise _credentials_error

    student_result = db.execute(select(Student).where(Student.id == student_id))
    student = student_result.scalar_one_or_none()
    if student is None or student.status != StudentStatus.ACTIVE:
        raise _credentials_error

    return student


def get_current_session_id(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
) -> uuid.UUID:
    """
    Lightweight companion to get_current_student — used where a route
    needs to know *which session* made the request (logout, and marking
    "is_current" in the /students/me/sessions list) without a second
    full authorization check.
    """
    try:
        payload = decode_access_token(credentials.credentials)
        return uuid.UUID(payload["session_id"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise _credentials_error
