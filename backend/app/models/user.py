"""
The single identity table. Replaces the separate `students` and `teachers`
tables' identity/credential columns. There is exactly one login per person:
one username, one password, one row here -- regardless of whether they are
currently a student, a teacher, or an admin.

Role storage: role_id is a foreign key into the roles table (see
models/role.py) -- not an enum column. That's a deliberate choice for the
Admin issue (per-role descriptions need to be stored and editable later).

Role-specific columns:
    class_level                only meaningful when role == STUDENT
    phone_number, specialization   only meaningful when role == TEACHER
    (ADMIN has no extra columns -- it's a permission level, not a profile)

Both sets of role-specific columns are nullable ON PURPOSE. A role switch
(see services/user_service.py / admin_service.py) clears whichever set no
longer applies and resets the other set to blank -- "erase and start over,"
exactly as specified. Neither set is ever populated for the "wrong" role;
that invariant is enforced in code, not by a database constraint, to keep
this migration-friendly for you to write yourself.

Authorization reads the ROLE CLAIM ON THE JWT (a UserRole string name, see
models/role.py), not a live read of this row's role_id, on every request
(see api/deps.py). That is deliberate: an admin changing someone's role_id
must NOT retroactively invalidate a token that's already out there -- the
person keeps whatever their current token grants until it's used to log out
or it naturally expires. This column is what the NEXT login reads.
"""
import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, text
from sqlalchemy import Enum as PgEnum
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.role import AccountStatus, Role


class ClassLevel(str, Enum):
    """
    Tanzania's education levels, in order. Fixed on purpose -- not free
    text -- so the curriculum domain can reliably filter subjects and
    topics by level later. Only meaningful while role == STUDENT.
    """
    STD_1 = "STD_1"
    STD_2 = "STD_2"
    STD_3 = "STD_3"
    STD_4 = "STD_4"
    STD_5 = "STD_5"
    STD_6 = "STD_6"
    STD_7 = "STD_7"
    FORM_1 = "FORM_1"
    FORM_2 = "FORM_2"
    FORM_3 = "FORM_3"
    FORM_4 = "FORM_4"
    FORM_5 = "FORM_5"
    FORM_6 = "FORM_6"


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        # Case is preserved for display, but uniqueness is enforced on the
        # lowercased value -- "Amina" and "amina" can't become two separate
        # accounts. One index, for everyone -- there is exactly one login
        # identifier in this system now (username); email is optional,
        # informational, and never used to authenticate.
        Index("ix_users_username_lower", text("lower(username)"), unique=True),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    username: Mapped[str] = mapped_column(String(32), nullable=False)
    # Optional everywhere: many students won't have one; teachers usually
    # will, but it is still never required and never used to log in.
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    role: Mapped["Role"] = relationship(foreign_keys=[role_id])
    status: Mapped[AccountStatus] = mapped_column(
        PgEnum(AccountStatus, name="account_status"),
        nullable=False,
        default=AccountStatus.ACTIVE,
        server_default=AccountStatus.ACTIVE.value,
    )

    # --- STUDENT-only. NULL whenever role == TEACHER. ---
    class_level: Mapped[ClassLevel | None] = mapped_column(
        PgEnum(ClassLevel, name="class_level"), nullable=True
    )

    # --- TEACHER-only. NULL whenever role == STUDENT. ---
    phone_number: Mapped[str | None] = mapped_column(String(32), nullable=True)
    specialization: Mapped[str | None] = mapped_column(String(120), nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    sessions: Mapped[list["UserSession"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class UserSession(Base):
    """
    One row per *login*, not per physical device -- lab machines are shared,
    so hardware fingerprinting would be both unreliable and the wrong model.
    Both students and teachers get sessions now (previously only students
    did); this is what lets a logout on a shared lab PC take effect
    immediately, for anyone, regardless of role.

    role_id is a SNAPSHOT of user.role_id at the moment this session was
    created, not a live reference. Every access token issued for this
    session (the original one AND every refreshed one) carries the matching
    role NAME (via Role.name) as its role claim. This is what makes "an
    admin changing someone's role doesn't affect them until they log out"
    true for the session's entire lifetime, not just its first access
    token -- a silent background token refresh must not be able to quietly
    upgrade or downgrade what someone can do. Only a brand new login (a new
    session) picks up a changed role.
    """
    __tablename__ = "user_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    role: Mapped["Role"] = relationship(foreign_keys=[role_id])

    device_label: Mapped[str | None] = mapped_column(String(255), nullable=True)
    refresh_token_hash: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    last_activity_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    revoked: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    user: Mapped["User"] = relationship(back_populates="sessions")
