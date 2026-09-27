"""
Shared FastAPI dependencies: DB session + current-authenticated-student.
"""
import uuid
from collections.abc import Generator

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import decode_access_token
from app.models.student import Student, StudentSession, StudentStatus

# tokenUrl points Swagger's "Authorize" button at POST /auth/token (the
# OAuth2-form adapter in routes/auth.py) -- it does NOT change how a
# real client authenticates. A real client still calls POST /auth/login
# with JSON and sends the resulting access_token as a normal Bearer
# header; this scheme only affects how the *docs page* collects
# credentials.
_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

_credentials_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_db() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session


def get_current_student(
    token: str = Depends(_oauth2_scheme),
    db: Session = Depends(get_db),
) -> Student:
    try:
        payload = decode_access_token(token)
        student_id = uuid.UUID(payload["sub"])
        session_id = uuid.UUID(payload["session_id"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise _credentials_error

    session_row = db.execute(
        select(StudentSession).where(StudentSession.id == session_id)
    ).scalar_one_or_none()
    if session_row is None or session_row.revoked:
        raise _credentials_error

    student = db.execute(
        select(Student).where(Student.id == student_id)
    ).scalar_one_or_none()
    if student is None or student.status != StudentStatus.ACTIVE:
        raise _credentials_error

    return student


def get_current_session_id(
    token: str = Depends(_oauth2_scheme),
) -> uuid.UUID:
    try:
        payload = decode_access_token(token)
        return uuid.UUID(payload["session_id"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise _credentials_error