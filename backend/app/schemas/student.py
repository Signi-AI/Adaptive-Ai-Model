"""
Pydantic request/response schemas for the Student domain.

Nothing here ever includes password_hash or refresh_token_hash — the
issue is explicit that API responses must not leak sensitive fields, so
those columns simply have no corresponding field in any *Public schema.
"""
from typing import Optional
import uuid
from datetime import datetime

from fastapi import Form
from pydantic import BaseModel, ConfigDict, Field

from app.models.student import ClassLevel, StudentStatus

class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=8, max_length=128)
    class_level: ClassLevel

class LoginRequest(BaseModel):
    username: str = Field(..., description="The user's email or identifier")
    password: str = Field(..., description="The user's account password")
    device_label: Optional[str] = Field(None, description="Identifier for the login device")

    # This classmethod converts form data fields into your Pydantic schema
    @classmethod
    def as_form(
        cls,
        username: str = Form(...),
        password: str = Form(...),
        device_label: Optional[str] = Form(None)
    ):
        return cls(username=username, password=password, device_label=device_label)



class RefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: datetime


class StudentPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str
    full_name: str
    class_level: ClassLevel
    status: StudentStatus
    created_at: datetime
    last_login_at: datetime | None


class StudentUpdate(BaseModel):
    """Only the fields a student is allowed to change about themselves."""
    full_name: str | None = Field(default=None, min_length=2, max_length=120)
    class_level: ClassLevel | None = None


class SessionPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    device_label: str | None
    created_at: datetime
    last_activity_at: datetime
    expires_at: datetime
    revoked: bool
    is_current: bool = False
