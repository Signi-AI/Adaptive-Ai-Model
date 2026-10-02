"""
Pydantic schemas for the Teacher domain.

Nothing here ever includes password_hash. The progress/attempt schemas are
the *contract* the Learning/Adaptation domain is expected to fill (see
app/services/teacher_learning_adapter.py) -- the Teacher domain only reads
and displays those results, it never computes them.

Field-level cleaning/validation (strip, blank checks, phone format) lives in
app/core/validators.py, NOT here -- these validators are thin wrappers so the
exact same logic is reusable from user_service.py (see create_teacher_user,
which is called directly by the seed script and tests, bypassing Pydantic
entirely).

Login/token shapes are shared across roles now -- see schemas/auth.py. There
is no more separate TeacherTokenResponse; teachers get a TokenResponse from
the same POST /auth/login everyone else uses.
"""
import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.core.validators import (
    clean_full_name,
    clean_optional_phone,
    clean_optional_text,
    clean_required_text,
    role_name_from_value,
)
from app.models.role import AccountStatus, UserRole
from app.models.user import ClassLevel


# --------------------------------------------------------------------------
# Profile
# --------------------------------------------------------------------------

class TeacherPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str
    email: str | None
    full_name: str
    phone_number: str | None
    specialization: str | None
    status: AccountStatus
    role: UserRole
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None

    @field_validator("role", mode="before")
    @classmethod
    def _extract_role(cls, v):
        return role_name_from_value(v)


class TeacherUpdate(BaseModel):
    """
    Only what a teacher may change about themselves. email, status and id are
    deliberately absent, so sending them in a PATCH body has no effect.
    Send phone_number / specialization as null (or "") to clear them.
    """
    full_name: str | None = Field(default=None, max_length=120)
    phone_number: str | None = Field(default=None, max_length=32)
    specialization: str | None = Field(default=None, max_length=120)

    @field_validator("full_name")
    @classmethod
    def _clean_full_name(cls, v: str | None) -> str:
        return clean_full_name(v)

    @field_validator("phone_number")
    @classmethod
    def _clean_phone(cls, v: str | None) -> str | None:
        return clean_optional_phone(v)

    @field_validator("specialization")
    @classmethod
    def _clean_specialization(cls, v: str | None) -> str | None:
        return clean_optional_text(v)


# --------------------------------------------------------------------------
# Learning-domain contract (progress / attempts) -- consumed, not computed
# --------------------------------------------------------------------------

class TopicProgress(BaseModel):
    topic: str
    attempts_count: int = 0
    correct_count: int = 0
    incorrect_count: int = 0
    mastery: float | None = None


class SubjectProgress(BaseModel):
    subject: str
    mastery: float | None = None
    topics: list[TopicProgress] = []


class StudentProgressReport(BaseModel):
    student_id: uuid.UUID
    # False until the Learning domain supplies real data, so a frontend can
    # say "no learning data yet" instead of showing fake zeros.
    learning_data_available: bool = False
    overall_progress: float | None = None
    subjects: list[SubjectProgress] = []
    strengths: list[str] = []
    weaknesses: list[str] = []
    recommendations: list[str] = []


class AttemptSummary(BaseModel):
    id: uuid.UUID
    subject: str | None = None
    topic: str | None = None
    result: str  # e.g. CORRECT / INCORRECT -- owned by the Learning domain
    score: float | None = None
    attempted_at: datetime


class AttemptDetail(AttemptSummary):
    question: str
    student_answer: str
    expected_answer: str | None = None
    # AI/system feedback -- kept distinct from human teacher guidance.
    ai_feedback: str | None = None
    session_id: uuid.UUID | None = None


# --------------------------------------------------------------------------
# Students as seen by a teacher
# --------------------------------------------------------------------------

class AssignedStudentSummary(BaseModel):
    student_id: uuid.UUID
    full_name: str
    class_level: ClassLevel | None
    overall_progress: float | None = None
    # Until the Learning domain reports activity, this is the student's last login.
    last_activity_at: datetime | None = None
    assigned_at: datetime


class StudentProfileForTeacher(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str
    full_name: str
    class_level: ClassLevel | None
    status: AccountStatus
    created_at: datetime
    last_login_at: datetime | None


# --------------------------------------------------------------------------
# Human guidance
# --------------------------------------------------------------------------

class GuidanceCreate(BaseModel):
    guidance_text: str = Field(min_length=1, max_length=4000)
    subject: str | None = Field(default=None, max_length=120)
    topic: str | None = Field(default=None, max_length=120)
    attempt_id: uuid.UUID | None = None

    @field_validator("guidance_text")
    @classmethod
    def _not_blank(cls, v: str) -> str:
        return clean_required_text(v, field_name="guidance_text")

    @field_validator("subject", "topic")
    @classmethod
    def _blank_to_none(cls, v: str | None) -> str | None:
        return clean_optional_text(v)


class GuidancePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    teacher_id: uuid.UUID
    student_id: uuid.UUID
    subject: str | None
    topic: str | None
    attempt_id: uuid.UUID | None
    guidance_text: str
    is_read: bool
    created_at: datetime
    # Always HUMAN_TEACHER: this record is never AI feedback.
    source: Literal["HUMAN_TEACHER"] = "HUMAN_TEACHER"


class StudentOverview(BaseModel):
    profile: StudentProfileForTeacher
    progress: StudentProgressReport
    recent_attempts: list[AttemptSummary]
    recent_guidance: list[GuidancePublic]
