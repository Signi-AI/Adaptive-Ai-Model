"""
GET    /students/me
PATCH  /students/me
GET    /students/me/sessions
DELETE /students/me/sessions/{session_id}

Every route here requires get_current_student -- authenticated AND the
token's role claim is STUDENT. A teacher's token gets 403 here, even if
that same person was a student a moment ago and even if their DB row's
live role has since changed -- see api/deps.py for why that's deliberate.
"""
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_session_id, get_current_student, get_db
from app.models.user import User
from app.schemas.student import SessionPublic, StudentPublic, StudentUpdate
from app.services import user_service

router = APIRouter(prefix="/students", tags=["students"])


@router.get("/me", response_model=StudentPublic)
def read_own_profile(current_student: User = Depends(get_current_student)):
    return current_student


@router.patch("/me", response_model=StudentPublic)
def update_own_profile(
    payload: StudentUpdate,
    current_student: User = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    return user_service.update_profile(db, current_student, payload)


@router.get("/me/sessions", response_model=list[SessionPublic])
def list_own_sessions(
    current_student: User = Depends(get_current_student),
    current_session_id: uuid.UUID = Depends(get_current_session_id),
    db: Session = Depends(get_db),
):
    sessions = user_service.list_sessions(db, current_student.id)
    result = []
    for s in sessions:
        public = SessionPublic.model_validate(s)
        public.is_current = s.id == current_session_id
        result.append(public)
    return result


@router.delete("/me/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_own_session(
    session_id: uuid.UUID,
    current_student: User = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    user_service.revoke_session(db, current_student.id, session_id)
