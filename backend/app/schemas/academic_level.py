from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AcademicLevelBase(BaseModel):
    name: str
    code: str
    description: str | None = None
    active: bool = True


class AcademicLevelCreate(AcademicLevelBase):
    pass


class AcademicLevelUpdate(BaseModel):
    name: str | None = None
    code: str | None = None
    description: str | None = None
    active: bool | None = None


class AcademicLevelResponse(AcademicLevelBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)