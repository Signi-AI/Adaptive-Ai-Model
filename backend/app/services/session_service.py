"""
services/session_service.py

Records topic-selection events and retrieves the most recent one per
student. Nothing here decides whether a student *should* resume a
topic or what to teach them next - that's recommendation/AI-teaching
logic, out of scope here same as everywhere else it's come up.
"""

from sqlalchemy.orm import Session

from app.models.learning_session import LearningSession


def record_session(
    db: Session, student_id: int, subject_id: int, topic_id: int
) -> LearningSession:
    session = LearningSession(
        student_id=student_id,
        subject_id=subject_id,
        topic_id=topic_id,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_last_session(db: Session, student_id: int) -> LearningSession | None:
    return (
        db.query(LearningSession)
        .filter(LearningSession.student_id == student_id)
        .order_by(LearningSession.started_at.desc())
        .first()
    )