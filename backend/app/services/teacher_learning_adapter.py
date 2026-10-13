"""
The ONLY place the Teacher domain touches Learning/Adaptation data.

The Learning domain (progress, mastery, strengths/weaknesses, attempts,
recommendations) does not exist yet, so these three functions return honest
"no data" results instead of invented numbers. When that domain is built,
replace the bodies below with calls into its services and return the same
schema objects -- nothing else in the Teacher domain has to change, and the
Teacher domain never computes mastery or adaptation itself.

teacher_service calls these through the module (teacher_learning_adapter.x),
so they can be swapped out in tests.
"""
import uuid

from sqlalchemy.orm import Session

from app.schemas.teacher import AttemptDetail, AttemptSummary, StudentProgressReport


def get_student_progress(db: Session, student_id: uuid.UUID) -> StudentProgressReport:
    return StudentProgressReport(student_id=student_id, learning_data_available=False)


def list_student_attempts(
    db: Session, student_id: uuid.UUID, *, limit: int, offset: int
) -> list[AttemptSummary]:
    return []


def get_student_attempt(
    db: Session, student_id: uuid.UUID, attempt_id: uuid.UUID
) -> AttemptDetail | None:
    """Must return None unless the attempt exists AND belongs to student_id."""
    return None
