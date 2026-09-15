"""
schemas/learning.py

I/O contracts for the Subject -> Topic -> Lesson hierarchy. Read-only
for this issue on purpose — no *Create schemas here. Curriculum
content is seeded (scripts/seed_database.py), not written through
student-facing endpoints. See services/learning_service.py for why.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SubjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None
    created_at: datetime


class TopicRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject_id: int
    name: str
    description: str | None = None
    created_at: datetime


class LessonRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    topic_id: int
    title: str
    content: str
    order_index: int
    created_at: datetime
