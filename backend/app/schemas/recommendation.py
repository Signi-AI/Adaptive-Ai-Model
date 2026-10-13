"""schemas/recommendation.py  (Issue 08)

RecommendationOut answers the four questions from the issue:
  What should I study?  -> topic_name / subject_name
  Why?                  -> reason (+ reason_code)
  For which topic?      -> topic_id
  What action?          -> type + action (+ difficulty)
"""

from datetime import datetime

from pydantic import BaseModel, field_validator

from app.core.curriculum_ids import SubjectId, TopicId
from app.core.learning_enums import (
    Difficulty,
    RecommendationPriority,
    RecommendationStatus,
    RecommendationType,
)
from app.services.recommendation_rules import STUDENT_SETTABLE


class RecommendationOut(BaseModel):
    id: int
    subject_id: SubjectId
    subject_name: str
    topic_id: TopicId
    topic_name: str
    related_topic_id: TopicId | None = None
    type: RecommendationType
    action: str
    reason: str
    reason_code: str
    priority: RecommendationPriority
    difficulty: Difficulty | None = None
    status: RecommendationStatus
    adaptive_decision_id: int | None = None
    created_at: datetime
    updated_at: datetime


class RecommendationStatusUpdate(BaseModel):
    status: RecommendationStatus

    @field_validator("status")
    @classmethod
    def _student_may_set(cls, value: RecommendationStatus) -> RecommendationStatus:
        if value not in STUDENT_SETTABLE:
            allowed = ", ".join(s.value for s in STUDENT_SETTABLE)
            raise ValueError(f"status must be one of: {allowed}")
        return value


class TeacherRecommendationContext(BaseModel):
    """What the AI orchestration layer receives for the topic being taught.

    `primary` is the structured backend plan the Artificial Teacher should
    follow instead of inventing its own. No prompt text here: the context
    builder decides how to present it.
    """

    topic_id: TopicId
    primary: RecommendationOut | None = None
    open: list[RecommendationOut] = []             # most urgent first
    recent_history: list[RecommendationOut] = []   # latest closed ones, newest first
