"""
Pydantic request/response schemas for the Student domain.

Registration lives here because it's inherently student-only -- the only
public signup path in this system, and it always creates role=STUDENT.
Login, refresh, and tokens are shared across roles now -- see
schemas/auth.py.

Nothing here ever includes password_hash or refresh_token_hash.
"""
import re
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.validators import role_name_from_value
from app.models.role import AccountStatus, UserRole
from app.models.user import ClassLevel

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


class StudentPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str
    full_name: str
    # Nullable: a user who was just demoted from teacher back to student
    # starts with no class_level, same as "erase and start over" for every
    # other role-specific field. Normal registration always sets a real one.
    class_level: ClassLevel | None
    status: AccountStatus
    role: UserRole
    created_at: datetime
    last_login_at: datetime | None

    @field_validator("role", mode="before")
    @classmethod
    def _extract_role(cls, v):
        return role_name_from_value(v)


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
