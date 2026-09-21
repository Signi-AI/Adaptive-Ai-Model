"""Progress service: loads a student's data and runs the performance analyzer.

This layer talks to the database. Every analysis rule lives in the analyzer.
Flow: API route -> ProgressService -> performance_analyzer
"""
from typing import List

from sqlalchemy.orm import Session

from app.adaptive.performance_analyzer import (
    DEFAULT_CONFIG,
    AnalyzerConfig,
    AttemptRecord,
    MasteryRecord,
    PerformanceSummary,
    build_summary,
)
from app.models.attempt import Attempt
from app.models.mastery import Mastery


def _to_attempt_record(attempt: Attempt) -> AttemptRecord:
    # Only place that maps Attempt columns to analyzer fields; adjust names here
    return AttemptRecord(
        topic_id=attempt.topic_id,
        is_correct=attempt.is_correct,
        created_at=attempt.created_at,
        question_id=attempt.question_id,
        response_time=attempt.response_time,
    )


def _to_mastery_record(row: Mastery) -> MasteryRecord:
    return MasteryRecord(topic_id=row.topic_id, mastery=row.mastery)


class ProgressService:
    def __init__(self, db: Session, config: AnalyzerConfig = DEFAULT_CONFIG):
        self.db = db
        self.config = config

    def _load_attempts(self, student_id: int) -> List[AttemptRecord]:
        rows = self.db.query(Attempt).filter(Attempt.student_id == student_id).all()
        return [_to_attempt_record(row) for row in rows]

    def _load_mastery(self, student_id: int) -> List[MasteryRecord]:
        rows = self.db.query(Mastery).filter(Mastery.student_id == student_id).all()
        return [_to_mastery_record(row) for row in rows]

    def get_performance_summary(self, student_id: int) -> PerformanceSummary:
        """Performance summary for one student (all zeros if they have no data)."""
        attempts = self._load_attempts(student_id)
        mastery = self._load_mastery(student_id)
        return build_summary(attempts, mastery, self.config)