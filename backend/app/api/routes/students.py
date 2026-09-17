"""
api/routes/students.py
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentRead
from app.services import student_service

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=list[StudentRead])
def read_all(db: Session = Depends(get_db)) -> list[StudentRead]:
    return db.query(Student).all()


@router.get("/{student_name}", response_model=StudentRead)
def read_student(student_name: str, db: Session = Depends(get_db)) -> StudentRead:
    student = db.query(Student).filter(Student.name == student_name).first()
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.post("", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)) -> StudentRead:
    return student_service.create_student(db, payload)


@router.put("/{student_name}", response_model=StudentRead)
def update_student(
    student_name: str, payload: StudentCreate, db: Session = Depends(get_db)
) -> StudentRead:
    student = db.query(Student).filter(Student.name == student_name).first()
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student_service.update_student(db, student, payload)


@router.delete("/{student_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_name: str, db: Session = Depends(get_db)) -> None:
    student = db.query(Student).filter(Student.name == student_name).first()
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    student_service.delete_student(db, student)
