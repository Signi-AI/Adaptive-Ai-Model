"""
Looks up and validates roles against the `roles` table -- nothing else in
the codebase should query that table directly. "Resolve role ID" (section
20 of the Admin issue) means: every other service gets a Role row by name
through get_role_by_name(), never by guessing an id.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role, UserRole

CORE_ROLES: dict[UserRole, str] = {
    UserRole.ADMIN: "System-level user and role management.",
    UserRole.TEACHER: "Supervises students, reviews progress, gives human guidance.",
    UserRole.STUDENT: "Learner using the Artificial Teacher system.",
}


def ensure_core_roles_exist(db: Session) -> None:
    """
    Idempotent. Called on app startup (see main.py) specifically so that
    ordinary student self-registration never fails just because nobody
    remembered to run a seed script first -- the three roles a running
    system needs are guaranteed to exist the moment the app is serving
    requests at all, independent of the separate admin-account seed script
    (scripts/seed_admin.py), which is about creating a real credentialed
    identity and is deliberately NOT automatic.
    """
    existing = {r.name for r in db.execute(select(Role)).scalars().all()}
    for role_enum, description in CORE_ROLES.items():
        if role_enum.value not in existing:
            db.add(Role(name=role_enum.value, description=description))
    db.commit()


def get_role_by_name(db: Session, name: UserRole) -> Role:
    role = db.execute(select(Role).where(Role.name == name.value)).scalar_one_or_none()
    if role is None:
        # Should only happen if ensure_core_roles_exist() was never run
        # against this database -- a real setup problem, not a user error.
        raise RuntimeError(
            f"Role '{name.value}' does not exist in the roles table. "
            "Call role_service.ensure_core_roles_exist() against this database."
        )
    return role


def list_roles(db: Session) -> list[Role]:
    return list(db.execute(select(Role).order_by(Role.id)).scalars().all())
