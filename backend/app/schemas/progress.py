"""schemas/progress.py  (Issue 06)

Progress (how far through the curriculum) is NOT mastery (how well it is
understood): a student can have lesson_completion = 1.0 and mastery 0.4.
"""

from pydantic import BaseModel

from app.core.curriculum_ids import AcademicLevelId, SubjectId, TopicId
from app.core.learning_enums import MasteryStatus


class TopicProgress(BaseModel):
    topic_id: TopicId
    topic_name: str
    subject_id: SubjectId
    academic_level_id: AcademicLevelId
    studied: bool                  # at least one lesson completed or question attempted
    lessons_total: int
    lessons_completed: int
    lesson_completion: float       # 0..1
    questions_attempted: int
    questions_correct: int
    accuracy: float                # 0..1
    mastery_score: float
    status: MasteryStatus
    strength: bool
    weakness: bool


class SubjectProgressSummary(BaseModel):
    subject_id: SubjectId
    subject_name: str
    topics_total: int
    topics_studied: int
    lessons_total: int
    lessons_completed: int
    completion: float              # lessons_completed / lessons_total
    questions_attempted: int
    questions_correct: int
    accuracy: float                # questions_correct / questions_attempted
    average_mastery: float         # mean mastery over topics that have attempts


class SubjectProgress(SubjectProgressSummary):
    topics: list[TopicProgress]


class OverallProgress(BaseModel):
    topics_total: int
    topics_studied: int
    lessons_total: int
    lessons_completed: int
    completion: float
    questions_attempted: int
    questions_correct: int
    accuracy: float
    average_mastery: float
    subjects: list[SubjectProgressSummary]