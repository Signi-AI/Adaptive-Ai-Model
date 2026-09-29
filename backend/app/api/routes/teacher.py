"""
POST /teachers/login
GET    /teachers/me
PATCH  /teachers/me
GET    /teachers/me/students
GET    /teachers/me/students/{student_id}
GET    /teachers/me/students/{student_id}/progress
GET    /teachers/me/students/{student_id}/attempts
GET    /teachers/me/students/{student_id}/attempts/{attempt_id}
POST   /teachers/me/students/{student_id}/guidance
GET    /teachers/me/students/{student_id}/guidance

Every route below /login depends on get_current_teacher (authenticated AND
role == TEACHER). Every student-scoped route then goes through the assignment
check in teacher_service.get_assigned_student.
"""
from typing import Annotated
import uuid

from fastapi import APIRouter, Depends, Form, Query, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.api.teacher_deps import get_current_teacher
from app.models.teacher import Teacher
from app.schemas.teacher import (
    AssignedStudentSummary,
    AttemptDetail,
    AttemptSummary,
    GuidanceCreate,
    GuidancePublic,
    StudentOverview,
    StudentProgressReport,
    TeacherPublic,
    TeacherTokenResponse,
    TeacherUpdate,
    TeacherTokenResponse,
)
from app.services import teacher_service
from app.models.student import ClassLevel
from app.api.teacher_deps import oauth2_scheme_teacher


router = APIRouter(prefix="/teachers", tags=["teachers"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="teachers/token") 

@router.post("/register", response_model=TeacherPublic, status_code=status.HTTP_201_CREATED)
def register(
    # 1. This grabs form_data.username and form_data.password
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    # 2. Add your custom mandatory registration fields here as separate Form parameters
    full_name: Annotated[str, Form()],
    email: Annotated[str, Form()],
    phone_number: Annotated[int, Form()],
    db: Session = Depends(get_db)
):
    """
    Registers a new student using OAuth2 form data alongside extra registration form fields.
    """
    # 3. Pass these clean form values into your service function
    return teacher_service.create_teacher(
        db=db, 
        full_name=full_name, 
        email=email, 
        password=form_data.password,
        phone_number=phone_number
        
        
    )


@router.get("/me")
def get_current_teacher_profile(token: str = Depends(oauth2_scheme)):
    """
    This endpoint will now show the lock icon in Swagger. Clicking it 
    will route credentials directly to your '/teachers/token' endpoint!
    """
    # Your dependency decoding and logic here
    return {"status": "authorized", "token": token}

@router.post("/login", response_model=TeacherTokenResponse)
def teacher_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Teacher login endpoint."""
    _, token, expires_at = teacher_service.authenticate_teacher(
        db, form_data.username, form_data.password
    )
    return TeacherTokenResponse(
        access_token=token, 
        expires_at=expires_at
    )


@router.post("/token", response_model=TeacherTokenResponse)
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Swagger UI compatibility token endpoint."""
    _, token, expires_at = teacher_service.authenticate_teacher(
        db, form_data.username, form_data.password, device_label="Swagger UI"
    )
    return TeacherTokenResponse(
        access_token=token, 
        expires_at=expires_at
    )

@router.get("/me", response_model=TeacherPublic)
def read_own_profile(current_teacher: Teacher = Depends(get_current_teacher)):
    return current_teacher


@router.patch("/me", response_model=TeacherPublic)
def update_own_profile(
    payload: TeacherUpdate,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    return teacher_service.update_profile(db, current_teacher, payload)


@router.get("/me/students", response_model=list[AssignedStudentSummary])
def list_my_students(
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    return teacher_service.list_assigned_students(db, current_teacher)


@router.get("/me/students/{student_id}", response_model=StudentOverview)
def read_student_overview(
    student_id: uuid.UUID,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    return teacher_service.get_student_overview(db, current_teacher, student_id)


@router.get("/me/students/{student_id}/progress", response_model=StudentProgressReport)
def read_student_progress(
    student_id: uuid.UUID,
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    return teacher_service.get_student_progress(db, current_teacher, student_id)


@router.get("/me/students/{student_id}/attempts", response_model=list[AttemptSummary])
def list_student_attempts(
    student_id: uuid.UUID,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    return teacher_service.list_student_attempts(
        db, current_teacher, student_id, limit=limit, offset=offset
    )


@router.get("/me/students/{student_id}/attempts/{attempt_id}", response_model=AttemptDetail)
def read_student_attempt(
    student_id: uuid.UUID,
    attempt_id: uuid.UUID,
    current_teacher: Teacher = Depends(get_current_teacher),
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
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    return teacher_service.create_guidance(db, current_teacher, student_id, payload)


@router.get("/me/students/{student_id}/guidance", response_model=list[GuidancePublic])
def list_student_guidance(
    student_id: uuid.UUID,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_teacher: Teacher = Depends(get_current_teacher),
    db: Session = Depends(get_db),
):
    return teacher_service.list_guidance(
        db, current_teacher, student_id, limit=limit, offset=offset
    )
