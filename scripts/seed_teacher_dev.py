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
"""
import os
import sys

from sqlalchemy import func, select

from backend.app.core.config import get_settings
from backend.app.core.database import SessionLocal
from backend.app.core.security import hash_password
from backend.app.models.student import ClassLevel, Student, StudentStatus
from backend.app.models.teacher import Teacher
from backend.app.services import teacher_service

DEMO_PASSWORD = os.environ.get("DEMO_SEED_PASSWORD", "development-only-password")

DEMO_TEACHER = {
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
        teacher = db.execute(
            select(Teacher).where(func.lower(Teacher.email) == DEMO_TEACHER["email"])
        ).scalar_one_or_none()
        if teacher is None:
            teacher = teacher_service.create_teacher(
                db, password=DEMO_PASSWORD, **DEMO_TEACHER
            )
            print(f"created teacher  {teacher.email}")
        else:
            print(f"teacher exists   {teacher.email}")

        for username, full_name, class_level, assign in DEMO_STUDENTS:
            student = db.execute(
                select(Student).where(func.lower(Student.username) == username)
            ).scalar_one_or_none()
            if student is None:
                student = Student(
                    username=username,
                    full_name=full_name,
                    password_hash=hash_password(DEMO_PASSWORD),
                    class_level=class_level,
                    status=StudentStatus.ACTIVE,
                )
                db.add(student)
                db.commit()
                db.refresh(student)
                print(f"created student  {username}")
            else:
                print(f"student exists   {username}")

            if assign:
                teacher_service.assign_student_to_teacher(db, teacher.id, student.id)
                print(f"  assigned {username} -> {teacher.email}")

    print()
    print("DEV ONLY. Teacher login: email 'teacher@example.com' (in the `username`")
    print("field of POST /teachers/login), password = DEMO_SEED_PASSWORD or the default")
    print("'development-only-password'.")


if __name__ == "__main__":
    main()
