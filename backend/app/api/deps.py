"""
Shared FastAPI dependencies: DB session + current-authenticated-user.

ONE OAuth2PasswordBearer scheme now (there used to be two -- one for
students, one named "TeacherOAuth2" purely to avoid a Swagger naming
collision). That workaround is gone because the duplication it was working
around is gone: everyone logs in through the same POST /auth/login.

get_current_student / get_current_teacher check the ROLE CLAIM ON THE JWT,
not a live database read of user.role. This is what makes "an admin
changing someone's role doesn't retroactively break their current session"
true -- see core/security.py's module docstring for the full reasoning.
Only account STATUS (active/suspended/deactivated) and session revocation
are checked live, on every request, same as before.
"""
import uuid

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import decode_access_token
from app.models.role import AccountStatus, UserRole
from app.models.user import User, UserSession

_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

_credentials_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(_oauth2_scheme),
    db: Session = Depends(get_db),
) -> tuple[User, UserRole]:
    """
    Returns (user, token_role). token_role is the role claim FROM THE TOKEN,
    which is what every route-facing dependency below authorizes against --
    not user.role, which may have since changed. See module docstring.
    """
    try:
        payload = decode_access_token(token)
        user_id = uuid.UUID(payload["sub"])
        session_id = uuid.UUID(payload["session_id"])
        token_role = UserRole(payload["role"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise _credentials_error

    # The session is looked up on every request, not just the JWT signature
    # checked. This is what lets a logout on a shared lab PC take effect
    # immediately instead of waiting for the access token to expire.
    session_row = db.execute(select(UserSession).where(UserSession.id == session_id)).scalar_one_or_none()
    if session_row is None or session_row.revoked:
        raise _credentials_error

    user = db.execute(select(User).where(User.id == user_id)).scalar_one_or_none()
    if user is None or user.status != AccountStatus.ACTIVE:
        raise _credentials_error

    return user, token_role


def get_current_student(auth: tuple[User, UserRole] = Depends(get_current_user)) -> User:
    user, token_role = auth
    if token_role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Student access required")
    return user


def get_current_student_id(
    current_student: User = Depends(get_current_student),
) -> uuid.UUID:
    """Return the authenticated student's ID for student-owned resources."""
    return current_student.id


def get_current_teacher(auth: tuple[User, UserRole] = Depends(get_current_user)) -> User:
    user, token_role = auth
    if token_role != UserRole.TEACHER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Teacher access required")
    return user


def get_current_admin(auth: tuple[User, UserRole] = Depends(get_current_user)) -> User:
    """This is require_admin() from the Admin issue's section 9 -- same
    shape as get_current_student / get_current_teacher on purpose, so
    nothing about how authorization works needed to change to add a third
    role, only a third thin wrapper."""
    user, token_role = auth
    if token_role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return user


def get_current_session_id(token: str = Depends(_oauth2_scheme)) -> uuid.UUID:
    """
    Lightweight companion used where a route needs to know *which session*
    made the request (logout, and marking "is_current" in the sessions
    list) without pulling the full user row again.
    """
    try:
        payload = decode_access_token(token)
        return uuid.UUID(payload["session_id"])
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise _credentials_error
