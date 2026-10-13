"""
api/routes/sessions.py

Fixed: replaced non-existent learning_service.get_student() with a direct
User lookup, and corrected student_id type from int to uuid.UUID to match
the actual model.
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.core.database import get_db
from app.models.user import User
from app.schemas.session import LastSessionRead
from app.services import session_service

router = APIRouter(tags=["sessions"])


@router.get("/students/{student_id}/last-session", response_model=LastSessionRead)
def get_last_session(student_id: uuid.UUID, db: Session = Depends(get_db)) -> LastSessionRead:
    student = db.get(User, student_id)
    if student is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

    session = session_service.get_last_session(db, student_id)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No session history found for this student",
        )

    return session