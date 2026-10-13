from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.academic_level import AcademicLevel
from app.models.subject import Subject
from app.models.topic import Topic
from app.models.lesson import Lesson
from app.models.learning_objective import LearningObjective


# =========================
# Academic Level CRUD
# =========================

def create_academic_level(
    db: Session,
    academic_level: AcademicLevel,
) -> AcademicLevel:
    db.add(academic_level)
    db.commit()
    db.refresh(academic_level)

    return academic_level


def get_academic_level(
    db: Session,
    academic_level_id: int,
) -> AcademicLevel | None:
    return db.get(AcademicLevel, academic_level_id)


def get_academic_levels(
    db: Session,
) -> list[AcademicLevel]:
    statement = select(AcademicLevel).order_by(AcademicLevel.id)

    return list(db.scalars(statement).all())


# =========================
# Subject CRUD
# =========================

def create_subject(
    db: Session,
    subject: Subject,
) -> Subject:
    db.add(subject)
    db.commit()
    db.refresh(subject)

    return subject


def get_subject(
    db: Session,
    subject_id: int,
) -> Subject | None:
    return db.get(Subject, subject_id)


def get_subjects(
    db: Session,
) -> list[Subject]:
    statement = select(Subject).order_by(Subject.id)

    return list(db.scalars(statement).all())


def get_subjects_by_academic_level(
    db: Session,
    academic_level_id: int,
) -> list[Subject]:
    statement = (
        select(Subject)
        .where(Subject.academic_level_id == academic_level_id)
        .order_by(Subject.id)
    )

    return list(db.scalars(statement).all())


# =========================
# Topic CRUD
# =========================

def create_topic(
    db: Session,
    topic: Topic,
) -> Topic:
    db.add(topic)
    db.commit()
    db.refresh(topic)

    return topic


def get_topic(
    db: Session,
    topic_id: int,
) -> Topic | None:
    return db.get(Topic, topic_id)


def get_topics_by_subject(
    db: Session,
    subject_id: int,
) -> list[Topic]:
    statement = (
        select(Topic)
        .where(Topic.subject_id == subject_id)
        .order_by(Topic.sequence)
    )

    return list(db.scalars(statement).all())


# =========================
# Lesson CRUD
# =========================

def create_lesson(
    db: Session,
    lesson: Lesson,
) -> Lesson:
    db.add(lesson)
    db.commit()
    db.refresh(lesson)

    return lesson


def get_lesson(
    db: Session,
    lesson_id: int,
) -> Lesson | None:
    return db.get(Lesson, lesson_id)


def get_lessons_by_topic(
    db: Session,
    topic_id: int,
) -> list[Lesson]:
    statement = (
        select(Lesson)
        .where(Lesson.topic_id == topic_id)
        .order_by(Lesson.sequence)
    )

    return list(db.scalars(statement).all())


# =========================
# Learning Objective CRUD
# =========================

def create_learning_objective(
    db: Session,
    objective: LearningObjective,
) -> LearningObjective:
    db.add(objective)
    db.commit()
    db.refresh(objective)

    return objective


def get_learning_objective(
    db: Session,
    objective_id: int,
) -> LearningObjective | None:
    return db.get(LearningObjective, objective_id)


def get_objectives_by_lesson(
    db: Session,
    lesson_id: int,
) -> list[LearningObjective]:
    statement = (
        select(LearningObjective)
        .where(LearningObjective.lesson_id == lesson_id)
        .order_by(LearningObjective.sequence)
    )

    return list(db.scalars(statement).all())