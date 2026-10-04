"""schemas/mastery.py  (Issue 06) -- learning-state schemas + the evidence the
Assessment/Attempt domain hands to MasteryService."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, model_validator

from app.core.curriculum_ids import LearningObjectiveId, SubjectId, TopicId
from app.core.learning_enums import MasteryStatus
from app.services.mastery_rules import DIFFICULTY_DEFAULT, DIFFICULTY_MAX, DIFFICULTY_MIN


class AttemptEvidence(BaseModel):
    """
    One completed attempt, as far as mastery is concerned. The Attempt/Assessment
    domain builds this after it has stored the attempt and evaluated the answer.

    attempt_id            any stable id of the stored attempt (int/UUID/str); used
                          only to make processing idempotent.
    score                 0..1 (1 = fully correct, partial credit allowed)
    topic_id / learning_objective_id
                          give at least one. If an objective is given the topic is
                          derived from it; if both are given they must agree.
    difficulty            1 (easy) .. 5 (hard)
    """

    student_id: UUID
    attempt_id: str | int | UUID
    score: float = Field(ge=0.0, le=1.0)
    is_correct: bool
    topic_id: TopicId | None = None
    learning_objective_id: LearningObjectiveId | None = None
    difficulty: int = Field(default=DIFFICULTY_DEFAULT, ge=DIFFICULTY_MIN, le=DIFFICULTY_MAX)
    attempted_at: datetime | None = None

    @property
    def attempt_ref(self) -> str:
        return str(self.attempt_id)

    @model_validator(mode="after")
    def _check_target_and_ref(self) -> "AttemptEvidence":
        if self.topic_id is None and self.learning_objective_id is None:
            raise ValueError("Provide topic_id or learning_objective_id")
        if not 0 < len(self.attempt_ref) <= 64:
            raise ValueError("attempt_id must be 1-64 characters when written as text")
        return self


class LearningState(BaseModel):
    """What we currently know about the student for one learning area."""

    mastery_score: float
    status: MasteryStatus
    attempts: int
    correct_attempts: int
    incorrect_attempts: int
    recent_performance: float          # mean outcome of the last few attempts
    recent_outcomes: list[float]       # newest first, up to RECENT_OUTCOMES_LIMIT
    strength: bool
    weakness: bool
    last_assessed_at: datetime | None = None


class TopicLearningState(LearningState):
    topic_id: TopicId
    topic_name: str
    subject_id: SubjectId


class ObjectiveLearningState(LearningState):
    learning_objective_id: LearningObjectiveId
    description: str


class TopicMasteryDetail(TopicLearningState):
    objectives: list[ObjectiveLearningState] = []


class StudentLearningState(BaseModel):
    topics: list[TopicLearningState]
    strengths: list[TopicLearningState]    # strongest first
    weaknesses: list[TopicLearningState]   # weakest first
