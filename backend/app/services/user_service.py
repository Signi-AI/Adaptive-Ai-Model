"""
Identity service for the unified User model: registration (always creates a
STUDENT -- the only public signup path), login/refresh/logout, profile
updates, and the actual point of this file -- promote_to_teacher /
demote_to_student.

This replaces the old student_service.py entirely (its auth logic is now
here, generalized) and the identity-related half of the old
teacher_service.py (authenticate_teacher, create_teacher). Teacher-specific
BUSINESS logic that isn't about identity -- assignments, guidance, student
overviews -- stays in teacher_service.py.

Role-switch design, read before changing anything here:

- promote_to_teacher / demote_to_student ERASE the data belonging to the
  role being left, and also clear the role being entered (a safety net, in
  case of any prior inconsistent state) -- "erase and start over," exactly
  as specified. Username and password are never touched -- there is one
  login per person, and it does not change when their role does.

- Neither function touches UserSession rows. An admin flipping someone's
  role must NOT retroactively invalidate a session that's already active --
  see core/security.py and api/deps.py for the full reasoning. The person
  keeps whatever their current token grants until they log out (or it
  expires); only their NEXT login reads the new role.

- Both functions refuse to "promote" someone already a teacher, or "demote"
  someone already a student -- this is a real state transition, not an
  idempotent field update, and the caller (the future Admin endpoint)
  should not be able to trigger it by accident.
"""
import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy import delete, func, select
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
from app.core.validators import clean_email, clean_full_name, clean_optional_phone, clean_optional_text
from app.models.chat_message import ChatMessage
from app.models.role import AccountStatus, UserRole
from app.models.teacher import TeacherGuidance, TeacherStudentAssignment
from app.models.user import ClassLevel, User, UserSession
from app.schemas.student import RegisterRequest
from app.schemas.teacher import TeacherUpdate
from app.schemas.student import StudentUpdate
from app.services import role_service


# --------------------------------------------------------------------------
# Registration (student-only -- the only public signup path)
# --------------------------------------------------------------------------

def register_student(db: Session, data: RegisterRequest) -> User:
    existing = db.execute(
        select(User).where(func.lower(User.username) == data.username.lower())
    ).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="That username is already taken")

    user = User(
        username=data.username,
        full_name=data.full_name,
        password_hash=hash_password(data.password),
        role_id=role_service.get_role_by_name(db, UserRole.STUDENT).id,
        class_level=data.class_level,
        status=AccountStatus.ACTIVE,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="That username is already taken")
    db.refresh(user)
    return user


# --------------------------------------------------------------------------
# Teacher account creation (internal -- no public route, per the issue;
# used by the dev seed script and tests)
# --------------------------------------------------------------------------

def create_teacher_user(
    db: Session,
    *,
    username: str,
    full_name: str,
    password: str,
    email: str | None = None,
    phone_number: str | None = None,
    specialization: str | None = None,
) -> User:
    # No Pydantic model in front of this call site -- validate directly,
    # same functions the request schemas use.
    try:
        full_name = clean_full_name(full_name)
        email = clean_email(email) if email else None
        phone_number = clean_optional_phone(phone_number)
        specialization = clean_optional_text(specialization)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc))

    existing = db.execute(
        select(User).where(func.lower(User.username) == username.lower())
    ).scalar_one_or_none()
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="That username is already taken")

    user = User(
        username=username,
        email=email,
        full_name=full_name,
        password_hash=hash_password(password),
        role_id=role_service.get_role_by_name(db, UserRole.TEACHER).id,
        phone_number=phone_number,
        specialization=specialization,
        status=AccountStatus.ACTIVE,
    )
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="That username is already taken")
    db.refresh(user)
    return user


# --------------------------------------------------------------------------
# Login / refresh / logout -- one flow, for every role
# --------------------------------------------------------------------------

def authenticate_and_create_session(
    db: Session, username: str, password: str, device_label: str | None
) -> tuple[User, UserSession, str, str, datetime]:
    """
    Returns (user, session, access_token, raw_refresh_token, access_expires_at).
    Same 401 for "unknown username" and "wrong password" so the endpoint
    can't be used to enumerate accounts. Works identically regardless of
    the account's role -- the token's role claim is set from user.role AS
    OF THIS LOGIN, then snapshotted onto the session (see UserSession.role).
    """
    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password"
    )

    user = db.execute(
        select(User).where(func.lower(User.username) == username.lower())
    ).scalar_one_or_none()
    if user is None:
        raise invalid_credentials
    if not verify_password(password, user.password_hash):
        raise invalid_credentials
    if user.status != AccountStatus.ACTIVE:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="This account is not active")

    raw_refresh_token = generate_refresh_token()
    session = UserSession(
        user_id=user.id,
        role_id=user.role_id,  # snapshot -- see UserSession.role_id docstring
        device_label=device_label,
        refresh_token_hash=hash_refresh_token(raw_refresh_token),
        expires_at=refresh_token_expiry(),
    )
    db.add(session)
    user.last_login_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(session)

    access_token, expires_at = create_access_token(
        user_id=str(user.id), session_id=str(session.id), role=UserRole(session.role.name)
    )
    return user, session, access_token, raw_refresh_token, expires_at


def refresh_session(db: Session, raw_refresh_token: str) -> tuple[str, str, datetime]:
    """
    Validates and rotates a refresh token. The new access token carries the
    SESSION's snapshotted role, not a fresh read of user.role -- a silent
    background refresh must not be able to change what someone can do.
    """
    invalid_token = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token"
    )

    token_hash = hash_refresh_token(raw_refresh_token)
    session = db.execute(
        select(UserSession).where(UserSession.refresh_token_hash == token_hash)
    ).scalar_one_or_none()

    if session is None or session.revoked:
        raise invalid_token

    now = datetime.now(timezone.utc)
    if session.expires_at.replace(tzinfo=timezone.utc) < now:
        raise invalid_token

    new_raw_refresh_token = generate_refresh_token()
    session.refresh_token_hash = hash_refresh_token(new_raw_refresh_token)
    session.expires_at = refresh_token_expiry()
    session.last_activity_at = now
    db.commit()

    access_token, expires_at = create_access_token(
        user_id=str(session.user_id), session_id=str(session.id), role=UserRole(session.role.name)
    )
    return access_token, new_raw_refresh_token, expires_at


def revoke_session(db: Session, user_id: uuid.UUID, session_id: uuid.UUID) -> None:
    session = db.execute(select(UserSession).where(UserSession.id == session_id)).scalar_one_or_none()
    if session is None or session.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    session.revoked = True
    session.revoked_at = datetime.now(timezone.utc)
    db.commit()


def list_sessions(db: Session, user_id: uuid.UUID) -> list[UserSession]:
    result = db.execute(
        select(UserSession).where(UserSession.user_id == user_id).order_by(UserSession.last_activity_at.desc())
    )
    return list(result.scalars().all())


# --------------------------------------------------------------------------
# Profile updates (works for either role's *Update schema -- both are just
# "the fields this person may change about themselves")
# --------------------------------------------------------------------------

def update_profile(db: Session, user: User, data: StudentUpdate | TeacherUpdate) -> User:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


# --------------------------------------------------------------------------
# Role switching -- the actual feature this file exists for
# --------------------------------------------------------------------------

def _erase_student_data(db: Session, user: User) -> None:
    """Wipes everything that only makes sense while someone is a student."""
    db.execute(delete(ChatMessage).where(ChatMessage.student_id == user.id))
    db.execute(delete(TeacherStudentAssignment).where(TeacherStudentAssignment.student_id == user.id))
    db.execute(delete(TeacherGuidance).where(TeacherGuidance.student_id == user.id))
    user.class_level = None


def _erase_teacher_data(db: Session, user: User) -> None:
    """Wipes everything that only makes sense while someone is a teacher."""
    db.execute(delete(TeacherStudentAssignment).where(TeacherStudentAssignment.teacher_id == user.id))
    db.execute(delete(TeacherGuidance).where(TeacherGuidance.teacher_id == user.id))
    user.phone_number = None
    user.specialization = None


def promote_to_teacher(db: Session, user_id: uuid.UUID) -> User:
    """
    Flips a STUDENT to TEACHER. Erases all student data (class_level, chat
    history, assignments/guidance received as a student) and starts the
    teacher side completely blank (no phone/specialization) -- fill those in
    afterward via PATCH /teachers/me. Username, password, and any currently
    active sessions are untouched.
    """
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    teacher_role = role_service.get_role_by_name(db, UserRole.TEACHER)
    if user.role_id == teacher_role.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is already a teacher")

    _erase_student_data(db, user)
    _erase_teacher_data(db, user)  # safety net -- guarantees a truly blank start
    user.role_id = teacher_role.id
    db.commit()
    db.refresh(user)
    return user


def demote_to_student(db: Session, user_id: uuid.UUID) -> User:
    """
    Flips a TEACHER back to STUDENT. Erases all teacher data (phone,
    specialization, every assignment/guidance they gave as a teacher) and
    starts the student side completely blank (no class_level) -- set it
    afterward via PATCH /students/me. Username, password, and any currently
    active sessions are untouched.
    """
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    student_role = role_service.get_role_by_name(db, UserRole.STUDENT)
    if user.role_id == student_role.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is already a student")

    _erase_teacher_data(db, user)
    _erase_student_data(db, user)  # safety net -- guarantees a truly blank start
    user.role_id = student_role.id
    db.commit()
    db.refresh(user)
    return user
