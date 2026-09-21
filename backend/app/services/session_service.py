"""
services/session_service.py

Records topic/lesson-selection events, retrieves the most recent one
per student, and tracks lesson completion. Nothing here decides
whether a student *should* resume a topic, what to teach them next,
or how well they're mastering it - that's recommendation/AI-teaching/
mastery logic, out of scope here same as everywhere else it's come up.
"""

from sqlalchemy.orm import Session

from app.models.learning_session import LearningSession
from app.models.lesson_completion import LessonCompletion


def record_session(
    db: Session,
    student_id: int,
    subject_id: int,
    topic_id: int,
    lesson_id: int | None = None,
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


def get_last_session(db: Session, student_id: int) -> LearningSession | None:
    """
    Ordered by started_at, then id, both descending. SQLite's
    CURRENT_TIMESTAMP has only one-second precision - a student
    moving from topic to lesson to lesson in quick succession can
    easily produce several rows with an identical started_at. Without
    the id tiebreaker, "most recent" would be decided arbitrarily by
    SQLite whenever that tie happens, not by actual recency.
    """
    return (
        db.query(LearningSession)
        .filter(LearningSession.student_id == student_id)
        .order_by(LearningSession.started_at.desc(), LearningSession.id.desc())
        .first()
    )


def mark_lesson_complete(db: Session, student_id: int, lesson_id: int) -> LessonCompletion:
    """
    Idempotent: calling this twice for the same student+lesson returns
    the existing row rather than creating a duplicate. The database's
    own unique constraint (see models/lesson_completion.py) is the
    real guarantee; this check just avoids an avoidable IntegrityError
    on the common case of a UI re-sending the same request.
    """
    existing = (
        db.query(LessonCompletion)
        .filter(
            LessonCompletion.student_id == student_id,
            LessonCompletion.lesson_id == lesson_id,
        )
        .first()
    )
    if existing is not None:
        return existing

    completion = LessonCompletion(student_id=student_id, lesson_id=lesson_id)
    db.add(completion)
    db.commit()
    db.refresh(completion)
    return completion


def get_completed_lesson_ids(
    db: Session, student_id: int, lesson_ids: list[int]
) -> set[int]:
    if not lesson_ids:
        return set()
    rows = (
        db.query(LessonCompletion.lesson_id)
        .filter(
            LessonCompletion.student_id == student_id,
            LessonCompletion.lesson_id.in_(lesson_ids),
        )
        .all()
    )
    return {row[0] for row in rows}