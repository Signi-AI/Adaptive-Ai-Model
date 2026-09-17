"""
schemas/student.py

I/O contracts for the Student model. StudentCreate is deliberately
narrow — name and class_level only. No credentials here (see
models/student.py for why).
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255,examples=["Comfotha Abdulkarim kalima"])
    class_level: str = Field(..., min_length=1, max_length=7, examples=["Form 2"])


class StudentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    class_level: str
    created_at: datetime
