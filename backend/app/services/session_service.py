"""
services/session_service.py

Records topic/lesson-selection events, retrieves the most recent one
per student, and tracks lesson completion. Nothing here decides
whether a student *should* resume a topic, what to teach them next,
or how well they're mastering it - that's recommendation/AI-teaching/
mastery logic, out of scope here same as everywhere else it's come up.
"""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.learning_session import LearningSession
from app.models.lesson_completion import LessonCompletion


def record_session(
    db: Session,
    student_id: uuid.UUID,
    subject_id: uuid.UUID,
    topic_id: uuid.UUID,
    lesson_id: uuid.UUID | None = None,
) -> LearningSession:
    session = LearningSession(
        student_id=student_id,
        subject_id=subject_id,
        topic_id=topic_id,
        lesson_id=lesson_id,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_last_session(db: Session, student_id: uuid.UUID) -> LearningSession | None:
    """
    Ordered by started_at, then id, both descending. PostgreSQL's
    timestamp precision is fine, but a student moving from topic to
    lesson in quick succession can produce rows with a very similar
    started_at. The id tiebreaker ensures deterministic ordering.
    """
    return db.execute(
        select(LearningSession)
        .where(LearningSession.student_id == student_id)
        .order_by(LearningSession.started_at.desc(), LearningSession.id.desc())
        .limit(1)
    ).scalar_one_or_none()


def mark_lesson_complete(db: Session, student_id: uuid.UUID, lesson_id: uuid.UUID) -> LessonCompletion:
    """
    Idempotent: calling this twice for the same student+lesson returns
    the existing row rather than creating a duplicate. The database's
    own unique constraint (see models/lesson_completion.py) is the
    real guarantee; this check just avoids an avoidable IntegrityError
    on the common case of a UI re-sending the same request.
    """
    existing = db.execute(
        select(LessonCompletion)
        .where(
            LessonCompletion.student_id == student_id,
            LessonCompletion.lesson_id == lesson_id,
        )
    ).scalar_one_or_none()
    if existing is not None:
        return existing

    completion = LessonCompletion(student_id=student_id, lesson_id=lesson_id)
    db.add(completion)
    db.commit()
    db.refresh(completion)
    return completion


def get_completed_lesson_ids(
    db: Session, student_id: uuid.UUID, lesson_ids: list[uuid.UUID]
) -> set[uuid.UUID]:
    if not lesson_ids:
        return set()
    rows = db.execute(
        select(LessonCompletion.lesson_id)
        .where(
            LessonCompletion.student_id == student_id,
            LessonCompletion.lesson_id.in_(lesson_ids),
        )
    ).all()
    return {row[0] for row in rows}