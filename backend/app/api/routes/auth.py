"""
POST /auth/register   -- always creates a STUDENT (the only public signup)
POST /auth/login       -- ONE login for every role
POST /auth/refresh
POST /auth/logout

There is no more POST /teachers/login. Login is shared now -- see
services/user_service.py's module docstring for why, and
api/deps.py's OAuth2PasswordBearer(tokenUrl="auth/login") for how Swagger's
Authorize button already points here for everyone.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_session_id, get_current_user, get_db
from app.schemas.auth import LoginRequest, RefreshRequest, TokenResponse
from app.schemas.student import RegisterRequest, StudentPublic
from app.services import user_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=StudentPublic, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    return user_service.register_student(db, payload)


@router.post("/login", response_model=TokenResponse)
def login(
    # Using Depends(LoginRequest.as_form) forces FastAPI to accept Form-Data
    # (what Swagger's Authorize dialog actually sends) while the route body
    # still works with LoginRequest like a normal Pydantic object. Works
    # identically for a student username or a teacher username -- there is
    # only one login identifier now.
    credentials: Annotated[LoginRequest, Depends(LoginRequest.as_form)],
    db: Session = Depends(get_db),
):
    _, _, access_token, refresh_token, expires_at = user_service.authenticate_and_create_session(
        db, credentials.username, credentials.password, credentials.device_label
    )
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, expires_at=expires_at)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    access_token, refresh_token, expires_at = user_service.refresh_session(db, payload.refresh_token)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token, expires_at=expires_at)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    auth=Depends(get_current_user),
    current_session_id=Depends(get_current_session_id),
    db: Session = Depends(get_db),
):
    current_user, _token_role = auth
    user_service.revoke_session(db, current_user.id, current_session_id)
