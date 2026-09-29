"""
Pydantic schemas for the Teacher domain.

Nothing here ever includes password_hash. The progress/attempt schemas are
the *contract* the Learning/Adaptation domain is expected to fill (see
app/services/teacher_learning_adapter.py) -- the Teacher domain only reads
and displays those results, it never computes them.
"""
import re
import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.student import ClassLevel, StudentStatus
from app.models.teacher import TeacherStatus

_PHONE_PATTERN = re.compile(r"^\+?[0-9 ()\-]{6,32}$")


# --------------------------------------------------------------------------
# Auth / profile
# --------------------------------------------------------------------------

class TeacherTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: datetime


class TeacherPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    full_name: str
    phone_number: str | None
    specialization: str | None
    status: TeacherStatus
    created_at: datetime
    updated_at: datetime
    last_login_at: datetime | None


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
        if v is None:
            raise ValueError("full_name cannot be null")
        v = v.strip()
        if len(v) < 2:
            raise ValueError("full_name must be at least 2 characters")
        return v

    @field_validator("phone_number")
    @classmethod
    def _clean_phone(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        if v == "":
            return None
        if not _PHONE_PATTERN.match(v):
            raise ValueError("phone_number must be 6-32 characters: digits, spaces, + ( ) -")
        return v

    @field_validator("specialization")
    @classmethod
    def _clean_specialization(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        return v or None


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
    class_level: ClassLevel
    overall_progress: float | None = None
    # Until the Learning domain reports activity, this is the student's last login.
    last_activity_at: datetime | None = None
    assigned_at: datetime


class StudentProfileForTeacher(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str
    full_name: str
    class_level: ClassLevel
    status: StudentStatus
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
        v = v.strip()
        if not v:
            raise ValueError("guidance_text cannot be blank")
        return v

    @field_validator("subject", "topic")
    @classmethod
    def _blank_to_none(cls, v: str | None) -> str | None:
        if v is None:
            return None
        v = v.strip()
        return v or None


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

