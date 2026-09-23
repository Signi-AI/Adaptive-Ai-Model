from pydantic import BaseModel
from typing import List


class TopicPerformance(BaseModel):
    """Performance summary for one topic."""
    topic_id: int
    topic_name: str
    mastery_score: float
    attempts_count: int
    correct_count: int


class ProgressResponse(BaseModel):
    """Overall progress response for a student."""
    student_id: int
    topics: List[TopicPerformance]