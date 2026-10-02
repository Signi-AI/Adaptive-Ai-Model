"""
Seeds the initial Admin account. Run once, by a human, deliberately --
unlike role seeding (see role_service.ensure_core_roles_exist, called
automatically on every app startup), this does NOT run automatically,
because it creates a real credentialed identity.

Required environment variables -- there is no hardcoded fallback password
here on purpose, unlike the demo teacher/student seed. The issue is
explicit: "Admin credentials must not be hard-coded into application
source code." A predictable default is effectively hard-coded, so this
script refuses to run without real values supplied:

    ADMIN_SEED_USERNAME
    ADMIN_SEED_PASSWORD
    ADMIN_SEED_EMAIL        (optional)
    ADMIN_SEED_FULL_NAME    (optional, defaults to "System Administrator")

Run from the project root:

    ADMIN_SEED_USERNAME=... ADMIN_SEED_PASSWORD=... python -m scripts.seed_admin

Idempotent: if a user with that username already exists, nothing is
created or changed -- this script never promotes an existing account and
never resets a password. If you need to recover admin access, that's a
deliberate separate operation, not a side effect of rerunning this script.
"""
import os
import sys

from sqlalchemy import func, select

from backend.app.core.database import SessionLocal
from backend.app.core.security import hash_password
from backend.app.models.role import UserRole
from backend.app.models.user import User
from backend.app.services import role_service


def main() -> None:
    username = os.environ.get("ADMIN_SEED_USERNAME")
    password = os.environ.get("ADMIN_SEED_PASSWORD")
    if not username or not password:
        sys.exit(
            "ADMIN_SEED_USERNAME and ADMIN_SEED_PASSWORD must both be set in the "
            "environment. Refusing to run with a hardcoded or guessable default "
            "for an admin account."
        )

    email = os.environ.get("ADMIN_SEED_EMAIL") or None
    full_name = os.environ.get("ADMIN_SEED_FULL_NAME", "System Administrator")

    with SessionLocal() as db:
        role_service.ensure_core_roles_exist(db)  # safe even if main.py's startup already did this

        existing = db.execute(
            select(User).where(func.lower(User.username) == username.lower())
        ).scalar_one_or_none()
        if existing is not None:
            print(f"User '{username}' already exists -- not creating a duplicate admin.")
            print(f"Current role: {existing.role.name}")
            return

        admin_role = role_service.get_role_by_name(db, UserRole.ADMIN)
        admin = User(
            username=username,
            email=email,
            full_name=full_name,
            password_hash=hash_password(password),
            role_id=admin_role.id,
        )
        db.add(admin)
        db.commit()
        print(f"Created initial admin '{username}'.")


if __name__ == "__main__":
    main()
