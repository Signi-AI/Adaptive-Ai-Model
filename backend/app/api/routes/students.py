"""
api/routes/students.py
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.models.student import Student
import app.models

from app.core.database import get_db
from app.schemas.student import StudentCreate, StudentRead
from app.services import student_service

router = APIRouter(prefix="/students", tags=["students"])


@router.get('/')
def read_all( db: Session = Depends(get_db)):
    return db.query(Student).all()


@router.post("", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)) -> StudentRead:
    return student_service.create_student(db, payload)


