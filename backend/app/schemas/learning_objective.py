from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LearningObjectiveBase(BaseModel):
    lesson_id: int
    description: str
    sequence: int
    is_active: bool = True


class LearningObjectiveCreate(LearningObjectiveBase):
    pass


class LearningObjectiveUpdate(BaseModel):
    lesson_id: int | None = None
    description: str | None = None
    sequence: int | None = None
    is_active: bool | None = None


class LearningObjectiveResponse(LearningObjectiveBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)