"""
api/routes/sessions.py
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from starlette import status

from app.core.database import get_db
from app.schemas.session import LastSessionRead
from app.services import learning_service, session_service

router = APIRouter(tags=["sessions"])


@router.get("/students/{student_id}/last-session", response_model=LastSessionRead)
def get_last_session(student_id: int, db: Session = Depends(get_db)) -> LastSessionRead:
    student = learning_service.get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    session = session_service.get_last_session(db, student_id)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No session history found for this student",
        )

    return session