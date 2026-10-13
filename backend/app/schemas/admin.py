"""
Schemas for the Admin domain. UserAdminView never includes password_hash,
refresh tokens, or anything session-related -- only what section 10 of the
issue actually asks for: identity, current role, account status.
"""
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.core.validators import role_name_from_value
from app.models.role import AccountStatus, UserRole


class UserAdminView(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str
    email: str | None
    full_name: str
    role: UserRole
    status: AccountStatus
    created_at: datetime
    last_login_at: datetime | None

    @field_validator("role", mode="before")
    @classmethod
    def _extract_role(cls, v):
        return role_name_from_value(v)


class RoleAssignment(BaseModel):
    """Body of PATCH /admin/users/{user_id}/role -- {"role": "TEACHER"}."""
    role: UserRole


class RolePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    is_active: bool
    created_at: datetime
