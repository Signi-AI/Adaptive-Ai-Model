from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LessonBase(BaseModel):
    topic_id: int
    title: str
    description: str | None = None
    content: str | None = None
    sequence: int
    estimated_learning_time: int | None = None
    is_active: bool = True


class LessonCreate(LessonBase):
    pass


class LessonUpdate(BaseModel):
    topic_id: int | None = None
    title: str | None = None
    description: str | None = None
    content: str | None = None
    sequence: int | None = None
    estimated_learning_time: int | None = None
    is_active: bool | None = None


class LessonResponse(LessonBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)