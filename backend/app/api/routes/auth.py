"""
POST /auth/register
POST /auth/login
POST /auth/refresh
POST /auth/logout
"""
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_session_id, get_current_student, get_db
from app.models.student import Student
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
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    return student_service.register_student(db, payload)

@router.post("/login", response_model=TokenResponse)
def login(
    # Using Depends(LoginRequest.as_form) forces FastAPI to accept Form-Data
    # while letting you interact with it as a clean Pydantic object!
    credentials: Annotated[LoginRequest, Depends(LoginRequest.as_form)],
    db: Session = Depends(get_db)
):
    _, _, access_token, refresh_token, expires_at = student_service.authenticate_and_create_session(
        db, 
        credentials.username, 
        credentials.password, 
        credentials.device_label
    )
    
    return TokenResponse(
        access_token=access_token, 
        refresh_token=refresh_token, 
        expires_at=expires_at
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
