"""
DEVELOPMENT / TEST DATA ONLY -- never run this against production.

Creates (idempotently):
  - 1 demo teacher
  - 3 demo students
  - assignments for the first 2 students (the 3rd is deliberately left
    unassigned, so you can watch the API deny access to it)

Run from the project root (the folder that contains `app/`):

    python -m scripts.seed_teacher_dev

Credentials are development placeholders. Override the password with the
DEMO_SEED_PASSWORD environment variable; nothing here is a real secret.
The script refuses to run when ENVIRONMENT=production.

Everyone logs in with a USERNAME now, including the demo teacher -- there is
one login identifier in this system, not a separate email-based one for
teachers. The demo teacher's email is stored too, but only as the optional,
informational field it always was.
"""
import os
import sys

from sqlalchemy import func, select

from backend.app.core.config import get_settings
from backend.app.core.database import SessionLocal
from backend.app.core.security import hash_password
from backend.app.models.role import UserRole
from backend.app.models.user import ClassLevel, User
from backend.app.services import role_service, teacher_service, user_service

DEMO_PASSWORD = os.environ.get("DEMO_SEED_PASSWORD", "development-only-password")

DEMO_TEACHER = {
    "username": "demo_teacher",
    "email": "teacher@example.com",
    "full_name": "Demo Teacher",
    "specialization": "Mathematics",
}

DEMO_STUDENTS = [
    # (username, full_name, class_level, assign_to_demo_teacher)
    ("demo_student_1", "Demo Student One", ClassLevel.FORM_2, True),
    ("demo_student_2", "Demo Student Two", ClassLevel.FORM_2, True),
    ("demo_student_3", "Demo Student Three (unassigned)", ClassLevel.FORM_3, False),
]


def main() -> None:
    settings = get_settings()
    if str(getattr(settings, "environment", "development")).lower() == "production":
        sys.exit("Refusing to seed development data while ENVIRONMENT=production.")

    with SessionLocal() as db:
        role_service.ensure_core_roles_exist(db)  # standalone script -- the app's lifespan never runs here

        teacher = db.execute(
            select(User).where(func.lower(User.username) == DEMO_TEACHER["username"])
        ).scalar_one_or_none()
        if teacher is None:
            teacher = user_service.create_teacher_user(db, password=DEMO_PASSWORD, **DEMO_TEACHER)
            print(f"created teacher  {teacher.username}")
        else:
            print(f"teacher exists   {teacher.username}")

        for username, full_name, class_level, assign in DEMO_STUDENTS:
            student = db.execute(
                select(User).where(func.lower(User.username) == username)
            ).scalar_one_or_none()
            if student is None:
                student = User(
                    username=username,
                    full_name=full_name,
                    password_hash=hash_password(DEMO_PASSWORD),
                    role_id=role_service.get_role_by_name(db, UserRole.STUDENT).id,
                    class_level=class_level,
                )
                db.add(student)
                db.commit()
                db.refresh(student)
                print(f"created student  {username}")
            else:
                print(f"student exists   {username}")

            if assign:
                teacher_service.assign_student_to_teacher(db, teacher.id, student.id)
                print(f"  assigned {username} -> {teacher.username}")

    print()
    print("DEV ONLY. Everyone logs in via POST /auth/login with a username.")
    print(f"Teacher: username 'demo_teacher', password '{DEMO_PASSWORD}'.")


if __name__ == "__main__":
    main()
