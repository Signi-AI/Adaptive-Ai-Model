from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TopicBase(BaseModel):
    subject_id: UUID
    name: str
    description: str | None = None
    sequence: int
    is_active: bool = True


class TopicCreate(TopicBase):
    pass


class TopicUpdate(BaseModel):
    subject_id: UUID | None = None
    name: str | None = None
    description: str | None = None
    sequence: int | None = None
    is_active: bool | None = None


class TopicResponse(TopicBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
