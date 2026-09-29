"""
Teacher authentication dependency.

Flow (matches the issue's diagram):
    JWT validation (shared decode_access_token)
        -> identify the teacher (sub must be an ACTIVE row in teachers)
        -> verify role == TEACHER
        -> allow the teacher endpoint

A student token is valid JWT but carries no TEACHER role, so it gets 403.
An expired / malformed / wrongly-signed token gets 401 from the shared decoder.
"""
import uuid

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.security import decode_access_token
from app.core.teacher_security import TEACHER_ROLE
from app.models.teacher import Teacher, TeacherStatus

# scheme_name must differ from the student scheme, otherwise both would share
# the default name "OAuth2PasswordBearer" and one would overwrite the other in
# the OpenAPI document. With a distinct name, Swagger's Authorize dialog shows
# a separate username/password form for teachers (username = the teacher's email).
_teacher_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="teachers/login", scheme_name="TeacherOAuth2"
)

_credentials_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


oauth2_scheme_teacher = OAuth2PasswordBearer(
    tokenUrl="teachers/token",  # Points to your teacher token route
    scheme_name="Teacher_Auth"   # Shows up distinctly in Swagger pop-up
)

def get_current_teacher(
    token: str = Depends(_teacher_oauth2_scheme),
    db: Session = Depends(get_db),
) -> Teacher:
    try:
        payload = decode_access_token(token)
        teacher_id = uuid.UUID(payload["sub"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise _credentials_error

    if payload.get("role") != TEACHER_ROLE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Teacher access required"
        )

    teacher = db.execute(select(Teacher).where(Teacher.id == teacher_id)).scalar_one_or_none()
    if teacher is None or teacher.status != TeacherStatus.ACTIVE:
        raise _credentials_error

    return teacher
