"""
schemas/session.py

Output shape for "what was this student last doing." Nests subject,
topic, and (if the session reached that far) lesson as lightweight
summaries rather than making the frontend chase more lookups just to
show "you were on Lesson 2 of Linear Equations (Mathematics)."
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SessionSubjectSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class SessionTopicSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class SessionLessonSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str


class LastSessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    subject: SessionSubjectSummary
    topic: SessionTopicSummary
    lesson: SessionLessonSummary | None = None
    started_at: datetime