"""
schemas/session.py

Output shape for "what was this student last doing." Nests subject
and topic as lightweight summaries rather than making the frontend
chase two more lookups just to show "you were on Linear Equations
(Mathematics)."
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


class LastSessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    student_id: int
    subject: SessionSubjectSummary
    topic: SessionTopicSummary
    started_at: datetime