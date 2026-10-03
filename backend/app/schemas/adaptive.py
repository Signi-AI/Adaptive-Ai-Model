"""schemas/adaptive.py  (Issue 07)

AdaptiveDecisionOut is the contract the other domains consume:
  * Question Service       -> action + difficulty + topic_id
  * Recommendation Service -> reason_code / reason + the numbers behind it
  * Artificial Teacher     -> action + topic_id + reason (+ difficulty as the
                              level to explain/revise at)
"""

from datetime import datetime

from pydantic import BaseModel, Field

from app.core.learning_enums import AdaptiveAction, Difficulty, ReasonCode, Trend


class AdaptiveDecisionOut(BaseModel):
    decision_id: int | None = None          # None for previews (nothing persisted)
    action: AdaptiveAction
    topic_id: int
    difficulty: Difficulty | None = None    # None for PROGRESS
    reason_code: ReasonCode
    reason: str
    mastery_score: float
    recent_performance: float
    trend: Trend
    attempts: int
    session_id: str | None = None
    decided_at: datetime


class AdaptiveDecideRequest(BaseModel):
    topic_id: int
    session_id: str | None = Field(default=None, max_length=64)