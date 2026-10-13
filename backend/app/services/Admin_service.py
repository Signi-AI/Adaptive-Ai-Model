"""
Admin-facing user and role management. Deliberately separate from
user_service.py (identity/auth) and teacher_service.py (teacher business
logic) -- per the issue's own suggested structure (section 20).

set_user_role() is THE operation behind PATCH /admin/users/{id}/role -- one
generic function for every transition (STUDENT<->TEACHER<->ADMIN), not a
separate function per pair, per the issue's explicit instruction not to
build a separate endpoint for every possible transition. It reuses the same
erase-and-start-over helpers user_service.py's promote_to_teacher /
demote_to_student already use and already have tests against, so there is
exactly one place that logic lives, not two that could drift apart.
"""
import uuid

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.role import AccountStatus, UserRole
from app.models.user import User
from app.services import role_service
from app.services.user_service import _erase_student_data, _erase_teacher_data


def list_users(db: Session,current_admin: User,  *, role: UserRole | None = None) -> list[User]:
    query = select(User).order_by(func.lower(User.username))
    if role is not None:
        role_row = role_service.get_role_by_name(db, role)
        query = query.where(User.role_id == role_row.id)
    return list(db.execute(query).scalars().all())


def get_user(db: Session, user_id: uuid.UUID) -> User:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


def count_active_admins(db: Session, *, excluding: uuid.UUID | None = None) -> int:
    admin_role = role_service.get_role_by_name(db, UserRole.ADMIN)
    query = select(func.count()).select_from(User).where(
        User.role_id == admin_role.id, User.status == AccountStatus.ACTIVE
    )
    if excluding is not None:
        query = query.where(User.id != excluding)
    return db.execute(query).scalar_one()


def set_user_role(db: Session, *, target_user_id: uuid.UUID, new_role: UserRole) -> User:
    """
    The one generic role-change operation. Validates the target exists,
    refuses a no-op switch (409, same as promote/demote already do),
    refuses to remove the last active admin, erases the data belonging to
    the role being left, starts the new role blank, and leaves username,
    password, and any active sessions completely untouched -- an admin
    flipping this does not retroactively affect a session already in use
    (see core/security.py's module docstring for the full reasoning; it's
    unchanged by this file's existence).

    Caller is responsible for the require_admin() check (see
    api/routes/admin.py) -- this function doesn't re-check who's calling,
    only what the result of the call would be.
    """
    user = get_user(db, target_user_id)
    new_role_row = role_service.get_role_by_name(db, new_role)

    if user.role_id == new_role_row.id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User already has the {new_role.value} role",
        )

    current_role_name = user.role.name

    # Final-admin protection -- the one hard rule in this function.
    if current_role_name == UserRole.ADMIN.value:
        remaining = count_active_admins(db, excluding=user.id)
        if remaining < 1:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Cannot change this user's role: they are the last active admin",
            )

    # Unconditionally erase BOTH student-only and teacher-only data, for
    # every transition, regardless of direction. This is deliberately not
    # branched on current/new role: each erase function only ever touches
    # rows belonging to THIS user and only ever clears fields that are
    # already blank if they don't apply -- calling the "wrong" one is a
    # harmless no-op. Doing it unconditionally removes an entire class of
    # directional bugs (erasing the role being entered instead of the role
    # being left, or vice versa) that a current-role/new-role branch would
    # otherwise risk. Admin has no role-specific fields, so there is
    # nothing extra to do when entering or leaving it.
    _erase_student_data(db, user)
    _erase_teacher_data(db, user)

    user.role_id = new_role_row.id
    db.commit()
    db.refresh(user)
    return user
