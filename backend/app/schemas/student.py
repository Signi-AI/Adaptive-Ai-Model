"""
Pydantic request/response schemas for the Student domain.

Nothing here ever includes password_hash or refresh_token_hash — the
issue is explicit that API responses must not leak sensitive fields, so
those columns simply have no corresponding field in any *Public schema.
"""
import re
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.student import ClassLevel, StudentStatus

_USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]{3,32}$")


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    full_name: str = Field(min_length=2, max_length=120)
    password: str = Field(min_length=8, max_length=128)
    class_level: ClassLevel

    @field_validator("username")
    @classmethod
    def username_format(cls, v: str) -> str:
        if not _USERNAME_PATTERN.match(v):
            raise ValueError(
                "Username must be 3-32 characters: letters, numbers, and underscores only"
            )
        return v


class LoginRequest(BaseModel):
    username: str
    password: str
    # Optional friendly label the frontend can send (e.g. from a device
    # picker in the UI) — purely for the student's own session list,
    # never used to make a security decision.
    device_label: str | None = Field(default=None, max_length=255)


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
