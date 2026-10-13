"""
Role storage and the small Python enums built on top of it.

Role is the actual source of truth for which roles exist -- a real table
with id/name/description/is_active, per the Admin issue's explicit choice
(descriptions need to be stored and editable later; an enum can't hold that).

UserRole stays as a plain string enum (STUDENT/TEACHER/ADMIN) and is NOT
database storage anymore -- User.role_id and UserSession.role_id are foreign
keys into the roles table below. UserRole exists purely at the Python/API
layer: it's what the JWT's role claim is, and what code compares against
(`token_role == UserRole.ADMIN`). This is deliberate: the JWT should carry a
portable, readable role NAME, not an internal database row id, and nothing
about token validation needs to change shape just because storage did --
see api/deps.py, which is untouched by this file's existence.

AccountStatus is unrelated to roles -- unchanged from before.
"""
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UserRole(str, Enum):
    STUDENT = "STUDENT"
    TEACHER = "TEACHER"
    ADMIN = "ADMIN"


class AccountStatus(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DEACTIVATED = "DEACTIVATED"


class Role(Base):
    """
    Exactly the three rows named in UserRole above, seeded once (see
    services/role_service.py::ensure_core_roles_exist, called on app
    startup -- see main.py -- so this table is never empty even before
    anyone thinks to run a seed script). name has no CHECK constraint
    restricting it to those three values on purpose: the whole reason this
    is a table and not an enum is that roles should be editable/extensible
    later. What DOES enforce "only real roles exist" is that there is no
    public endpoint that creates a Role row -- only GET /admin/roles reads
    them -- and User.role_id / UserSession.role_id are real foreign keys, so
    a user can never reference a role that isn't an actual row here.
    """
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default=text("true")
    )
