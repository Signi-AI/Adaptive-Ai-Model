from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TopicBase(BaseModel):
    subject_id: int
    name: str
    description: str | None = None
    sequence: int
    is_active: bool = True


class TopicCreate(TopicBase):
    pass


class TopicUpdate(BaseModel):
    subject_id: int | None = None
    name: str | None = None
    description: str | None = None
    sequence: int | None = None
    is_active: bool | None = None


class TopicResponse(TopicBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)