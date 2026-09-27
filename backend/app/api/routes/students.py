"""
GET    /students/me
PATCH  /students/me
GET    /students/me/sessions
DELETE /students/me/sessions/{session_id}
"""
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_session_id, get_current_student, get_db
from app.models.student import Student
from app.schemas.student import SessionPublic, StudentPublic, StudentUpdate
from app.services import student_service

router = APIRouter(prefix="/students", tags=["students"])


@router.get("/get_all")
def read_all(db: Session = Depends(get_db)):
    query = select(Student)
    result = db.execute(query)
    return result.scalars().all()


@router.get("/me", response_model=StudentPublic)
def read_own_profile(current_student: Student = Depends(get_current_student)):
    return current_student


@router.patch("/me", response_model=StudentPublic)
def update_own_profile(
    payload: StudentUpdate,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    return student_service.update_profile(db, current_student, payload)


@router.get("/me/sessions", response_model=list[SessionPublic])
def list_own_sessions(
    current_student: Student = Depends(get_current_student),
    current_session_id: uuid.UUID = Depends(get_current_session_id),
    db: Session = Depends(get_db),
):
    sessions = student_service.list_sessions(db, current_student.id)
    result = []
    for s in sessions:
        public = SessionPublic.model_validate(s)
        public.is_current = s.id == current_session_id
        result.append(public)
    return result


@router.delete("/me/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_own_session(
    session_id: uuid.UUID,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    student_service.revoke_session(db, current_student.id, session_id)
