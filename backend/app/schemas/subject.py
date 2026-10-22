from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SubjectBase(BaseModel):
    name: str
    code: str | None = None
    description: str | None = None
    academic_level_id: UUID
    active: bool = True


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    description: str | None = None
    academic_level_id: UUID | None = None
    active: bool | None = None


class SubjectResponse(SubjectBase):
    id: UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
