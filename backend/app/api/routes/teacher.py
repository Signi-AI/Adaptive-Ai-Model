"""
GET    /teachers/me
PATCH  /teachers/me
GET    /teachers/me/sessions              (new -- teachers now have real
DELETE /teachers/me/sessions/{session_id}  sessions, same as students)
GET    /teachers/me/students
GET    /teachers/me/students/{student_id}
GET    /teachers/me/students/{student_id}/progress
GET    /teachers/me/students/{student_id}/attempts
GET    /teachers/me/students/{student_id}/attempts/{attempt_id}
POST   /teachers/me/students/{student_id}/guidance
GET    /teachers/me/students/{student_id}/guidance

There is no POST /teachers/login anymore -- everyone logs in through
POST /auth/login now (see routes/auth.py and services/user_service.py).
Logging out is also shared: POST /auth/logout works regardless of role.

Every route below requires get_current_teacher (authenticated AND the
token's role claim is TEACHER). Every student-scoped route then goes
through the assignment check in teacher_service.get_assigned_student.
"""
import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_session_id, get_current_teacher, get_db
from app.models.user import User
from app.schemas.student import SessionPublic
from app.schemas.teacher import (
    AssignedStudentSummary,
    AttemptDetail,
    AttemptSummary,
    GuidanceCreate,
    GuidancePublic,
    StudentOverview,
    StudentProgressReport,
    TeacherPublic,
    TeacherUpdate,
)
from app.services import teacher_service, user_service

router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.get("/me", response_model=TeacherPublic)
def read_own_profile(current_teacher: User = Depends(get_current_teacher)):
    return current_teacher


@router.patch("/me", response_model=TeacherPublic)
def update_own_profile(
    payload: TeacherUpdate,
    current_teacher: User = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    return user_service.update_profile(db, current_teacher, payload)


@router.get("/me/sessions", response_model=list[SessionPublic])
def list_own_sessions(
    current_teacher: User = Depends(get_current_teacher),
    current_session_id: uuid.UUID = Depends(get_current_session_id),
    db: Session = Depends(get_db),
):
    sessions = user_service.list_sessions(db, current_teacher.id)
    result = []
    for s in sessions:
        public = SessionPublic.model_validate(s)
        public.is_current = s.id == current_session_id
        result.append(public)
    return result


@router.delete("/me/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def revoke_own_session(
    session_id: uuid.UUID,
    current_teacher: User = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    user_service.revoke_session(db, current_teacher.id, session_id)


@router.get("/me/students", response_model=list[AssignedStudentSummary])
def list_my_students(
    current_teacher: User = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    return teacher_service.list_assigned_students(db, current_teacher)


@router.get("/me/students/{student_id}", response_model=StudentOverview)
def read_student_overview(
    student_id: uuid.UUID,
    current_teacher: User = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    return teacher_service.get_student_overview(db, current_teacher, student_id)


@router.get("/me/students/{student_id}/progress", response_model=StudentProgressReport)
def read_student_progress(
    student_id: uuid.UUID,
    current_teacher: User = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    return teacher_service.get_student_progress(db, current_teacher, student_id)


@router.get("/me/students/{student_id}/attempts", response_model=list[AttemptSummary])
def list_student_attempts(
    student_id: uuid.UUID,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_teacher: User = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    return teacher_service.list_student_attempts(db, current_teacher, student_id, limit=limit, offset=offset)


@router.get("/me/students/{student_id}/attempts/{attempt_id}", response_model=AttemptDetail)
def read_student_attempt(
    student_id: uuid.UUID,
    attempt_id: uuid.UUID,
    current_teacher: User = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    return teacher_service.get_student_attempt(db, current_teacher, student_id, attempt_id)


@router.post(
    "/me/students/{student_id}/guidance",
    response_model=GuidancePublic,
    status_code=status.HTTP_201_CREATED,
)
def create_student_guidance(
    student_id: uuid.UUID,
    payload: GuidanceCreate,
    current_teacher: User = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    return teacher_service.create_guidance(db, current_teacher, student_id, payload)


@router.get("/me/students/{student_id}/guidance", response_model=list[GuidancePublic])
def list_student_guidance(
    student_id: uuid.UUID,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_teacher: User = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    return teacher_service.list_guidance(db, current_teacher, student_id, limit=limit, offset=offset)
