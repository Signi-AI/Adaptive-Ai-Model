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
import re
import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_session_id, get_current_student, get_db
from app.models.academic_level import AcademicLevel
from app.models.user import User
from app.schemas.student import SessionPublic, StudentCurriculum, StudentPublic, StudentUpdate
from app.services.curriculum_service import CurriculumService
from app.services import user_service

router = APIRouter(prefix="/students", tags=["students"])


def _level_key(value: object | None) -> str:
    """Make registration enum values match human-readable curriculum labels."""
    text = str(getattr(value, "value", value) or "").lower()
    text = re.sub(r"[^a-z0-9]", "", text)
    return text.replace("standard", "std")


@router.get("/me", response_model=StudentPublic)
def read_own_profile(current_student: User = Depends(get_current_student)):
    return current_student


@router.get("/me/curriculum", response_model=StudentCurriculum)
def read_own_curriculum(
    current_student: User = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    """Return only subjects belonging to the class saved at registration."""
    student_level = _level_key(current_student.class_level)
    if not student_level:
        return StudentCurriculum(academic_level_id=None, subjects=[])

    levels = db.execute(
        select(AcademicLevel).where(AcademicLevel.active.is_(True))
    ).scalars()
    academic_level = next(
        (
            level for level in levels
            if student_level in {_level_key(level.code), _level_key(level.name)}
        ),
        None,
    )
    if academic_level is None:
        return StudentCurriculum(academic_level_id=None, subjects=[])

    return StudentCurriculum(
        academic_level_id=academic_level.id,
        subjects=CurriculumService.get_subjects(db, academic_level.id),
    )


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
