"""
Pydantic schemas for the AI Teaching Session chat (MVP placeholder version).
"""
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.chat_message import ChatRole


class ChatMessageRequest(BaseModel):
    session_id: uuid.UUID
    message: str = Field(min_length=1, max_length=4000)


class ChatMessagePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    learning_session_id: uuid.UUID | None
    role: ChatRole
    content: str
    created_at: datetime


class ChatReplyResponse(BaseModel):
    session_id: uuid.UUID
    student_message: ChatMessagePublic
    ai_reply: ChatMessagePublic


class LearningSessionRequest(BaseModel):
    subject_id: uuid.UUID
    topic_id: uuid.UUID
    lesson_id: uuid.UUID | None = None


class LearningSessionPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    subject_id: uuid.UUID
    topic_id: uuid.UUID
    lesson_id: uuid.UUID | None
    started_at: datetime
    ended_at: datetime | None


class AttemptSubmissionRequest(BaseModel):
    session_id: uuid.UUID
    question_id: uuid.UUID
    student_answer: str = Field(min_length=1, max_length=4000)
    client_submission_id: uuid.UUID


class AttemptSubmissionResponse(BaseModel):
    attempt_id: uuid.UUID
    is_correct: bool
    score: float
    feedback: str
    mastery_score: float
    next_action: str
    recommendation_count: int


class PracticeQuestionPublic(BaseModel):
    id: uuid.UUID
    text: str
