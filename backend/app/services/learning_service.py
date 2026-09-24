"""
services/learning_service.py

Read-only retrieval for the Subject -> Topic -> Lesson hierarchy. No
create/update/delete here on purpose — curriculum content is seeded
(scripts/seed_database.py, a separate concern), not written through
student-facing API endpoints. A future "content management" need
(e.g. a teacher/admin UI) is a new, explicitly-scoped issue, not a
silent addition here.
"""

from sqlalchemy.orm import Session

from app.models.lesson import Lesson
from app.models.subject import Subject
from app.models.topic import Topic


def get_subjects(db: Session) -> list[Subject]:
    return db.query(Subject).order_by(Subject.name).all()


def get_subject(db: Session, subject_id: int) -> Subject | None:
    return db.get(Subject, subject_id)


def get_topics_by_subject(db: Session, subject_id: int) -> list[Topic]:
    return (
        db.query(Topic)
        .filter(Topic.subject_id == subject_id)
        .order_by(Topic.id)
        .all()
    )


def get_topic(db: Session, topic_id: int) -> Topic | None:
    return db.get(Topic, topic_id)


def get_lessons_by_topic(db: Session, topic_id: int) -> list[Lesson]:
    return (
        db.query(Lesson)
        .filter(Lesson.topic_id == topic_id)
        .order_by(Lesson.order_index)
        .all()
    )
