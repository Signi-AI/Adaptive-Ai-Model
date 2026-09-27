"""
POST /auth/register
POST /auth/login
POST /auth/token    <- OAuth2 form adapter, for Swagger's Authorize button
POST /auth/refresh
POST /auth/logout
"""
from typing import Annotated

from fastapi import APIRouter, Depends, Form, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_session_id, get_current_student, get_db
from app.models.student import ClassLevel, Student
from app.schemas.student import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    StudentPublic,
    TokenResponse,
)
from app.services import student_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=StudentPublic, status_code=status.HTTP_201_CREATED)
def register(
    # 1. This grabs form_data.username and form_data.password
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    # 2. Add your custom mandatory registration fields here as separate Form parameters
    full_name: Annotated[str, Form()],
    class_level: Annotated[ClassLevel, Form()],
    db: Session = Depends(get_db)
):
    """
    Registers a new student using OAuth2 form data alongside extra registration form fields.
    """
    # 3. Pass these clean form values into your service function
    return student_service.register_student(
        db=db, 
        username=form_data.username, 
        password=form_data.password, 
        full_name=full_name, 
        class_level=class_level
    )

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    _, _, access_token, refresh_token, expires_at = student_service.authenticate_and_create_session(
        db, payload.username, payload.password, payload.device_label
    )
    return TokenResponse(
        access_token=access_token, refresh_token=refresh_token, expires_at=expires_at
    )


@router.post("/token", response_model=TokenResponse)
def login_for_swagger(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Exists only so Swagger's "Authorize" button has a real endpoint to
    submit its username/password form to. Calls the exact same
    authenticate_and_create_session as /auth/login -- same password
    check, same session creation, same errors. Real clients should keep
    using POST /auth/login with JSON, which also lets them set a real
    device_label; this route hard-codes one since the OAuth2 form has no
    field for it.
    """
    _, _, access_token, refresh_token, expires_at = student_service.authenticate_and_create_session(
        db, form_data.username, form_data.password, device_label="Swagger UI"
    )
    return TokenResponse(
        access_token=access_token, refresh_token=refresh_token, expires_at=expires_at
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    access_token, refresh_token, expires_at = student_service.refresh_session(
        db, payload.refresh_token
    )
    return TokenResponse(
        access_token=access_token, refresh_token=refresh_token, expires_at=expires_at
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    current_student: Student = Depends(get_current_student),
    current_session_id=Depends(get_current_session_id),
    db: Session = Depends(get_db),
):
    student_service.revoke_session(db, current_student.id, current_session_id)