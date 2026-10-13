from pydantic import BaseModel
from typing import List


class LearningObjectiveNested(BaseModel):
    id: int
    description: str

    class Config:
        from_attributes = True


class LessonNested(BaseModel):
    id: int
    title: str
    objectives: List[LearningObjectiveNested] = []

    class Config:
        from_attributes = True


class TopicNested(BaseModel):
    id: int
    name: str
    lessons: List[LessonNested] = []

    class Config:
        from_attributes = True


class SubjectNested(BaseModel):
    id: int
    name: str
    topics: List[TopicNested] = []

    class Config:
        from_attributes = True


class CurriculumResponse(BaseModel):
    academic_level: dict
    subjects: List[SubjectNested] = []