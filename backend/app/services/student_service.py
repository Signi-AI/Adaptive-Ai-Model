"""
services/student_service.py

Business logic for Student. Routes stay thin — they call these
functions and translate results/errors to HTTP responses.
"""

from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate


def create_student(db: Session, payload: StudentCreate) -> Student:
    student = Student(name=payload.name, class_level=payload.class_level)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student
