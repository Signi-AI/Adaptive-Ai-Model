"""Structured, teaching-relevant context the BACKEND supplies to the Artificial Teacher.

The model never computes mastery, correctness, or recommendations. It only receives them.
Keep this file free of database code: the backend builds these objects from its own tables.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator

MasteryBand = Literal["unknown", "low", "medium", "high"]
RecentPerformance = Literal["unknown", "poor", "developing", "good", "excellent"]
Language = Literal["en", "sw"]

# Teaching-style bands only. These are NOT the BKT "mastered" threshold; the backend owns that.
# If the backend already has its own band, pass it as mastery_label and it wins.
LOW_BELOW = 0.40
HIGH_FROM = 0.70


def mastery_band(mastery: float | None) -> MasteryBand:
    if mastery is None:
        return "unknown"
    if mastery < LOW_BELOW:
        return "low"
    if mastery < HIGH_FROM:
        return "medium"
    return "high"


class StudentContext(BaseModel):
    display_name: str | None = Field(default=None, max_length=50)
    class_level: str = Field(..., min_length=1, max_length=20)  # e.g. "Form 2", "Std 5"
    mastery: float | None = Field(default=None, ge=0, le=1)
    mastery_label: MasteryBand | None = None
    strengths: list[str] = Field(default_factory=list, max_length=8)
    weaknesses: list[str] = Field(default_factory=list, max_length=8)
    recent_performance: RecentPerformance = "unknown"
    recommended_action: str | None = None  # backend-owned; see prompt_builder.resolve_action

    @field_validator("strengths", "weaknesses")
    @classmethod
    def _trim_items(cls, items: list[str]) -> list[str]:
        return [i.strip()[:80] for i in items if i and i.strip()]

    @property
    def band(self) -> MasteryBand:
        return self.mastery_label or mastery_band(self.mastery)


class Turn(BaseModel):
    role: Literal["student", "teacher"]
    content: str = Field(..., max_length=4000)


class AssessmentResult(BaseModel):
    """Backend-verified result of the student's last answer. The model must not re-judge it."""

    question: str
    student_answer: str
    is_correct: bool
    verified_answer: str | None = None
    verified_solution_steps: list[str] = Field(default_factory=list, max_length=12)
    reveal_answer: bool = False


def default_teaching_language(class_level: str, subject: str) -> Language:
    """Default language of instruction. Override per request with teaching_language.

    Assumption (confirm with your teachers): public primary (Std 1-7) is taught in Kiswahili,
    secondary (Form 1-6) in English; subject 'Kiswahili' is always Kiswahili and 'English' is
    always English. Private English-medium primary schools exist, so keep this overridable.
    """
    subj = subject.strip().casefold()
    if subj == "kiswahili":
        return "sw"
    if subj == "english":
        return "en"
    level = class_level.strip().casefold()
    if level.startswith(("std", "standard", "darasa")):
        return "sw"
    return "en"
