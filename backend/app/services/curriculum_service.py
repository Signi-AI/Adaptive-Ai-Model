from sqlalchemy.orm import Session

from app.crud import curriculum
from app.models.academic_level import AcademicLevel
from app.models.subject import Subject
from app.models.topic import Topic
from app.models.lesson import Lesson
from app.models.learning_objective import LearningObjective


class CurriculumService:

    # =========================
    # Academic Levels
    # =========================

    @staticmethod
    def get_academic_level(
        db: Session,
        academic_level_id: int,
    ):
        if academic_level := curriculum.get_academic_level(
            db,
            academic_level_id,
        ):
            return academic_level
        raise ValueError("Academic level not found")

    @staticmethod
    def get_academic_levels(db: Session):
        return curriculum.get_academic_levels(db)

    @staticmethod
    def create_academic_level(
        db: Session,
        name: str,
        code: str,
    ):
        existing_levels = curriculum.get_academic_levels(db)

        for level in existing_levels:
            if level.code.lower() == code.lower():
                raise ValueError(
                    "Academic level with this code already exists"
                )

        academic_level = AcademicLevel(
            name=name,
            code=code,
            is_active=True,
        )

        return curriculum.create_academic_level(
            db,
            academic_level,
        )

    # =========================
    # Subjects
    # =========================

    @staticmethod
    def get_subject(
        db: Session,
        subject_id: int,
    ):
        if subject := curriculum.get_subject(
            db,
            subject_id,
        ):
            return subject
        raise ValueError("Subject not found")

    @staticmethod
    def get_subjects(db: Session):
        return curriculum.get_subjects(db)

    @staticmethod
    def get_subjects_by_academic_level(
        db: Session,
        academic_level_id: int,
    ):
        CurriculumService.get_academic_level(
            db,
            academic_level_id,
        )

        return curriculum.get_subjects_by_academic_level(
            db,
            academic_level_id,
        )

    @staticmethod
    def create_subject(
        db: Session,
        name: str,
        code: str | None,
        description: str | None,
        academic_level_id: int,
    ):
        CurriculumService.get_academic_level(
            db,
            academic_level_id,
        )

        subjects = curriculum.get_subjects(db)

        for subject in subjects:
            if (
                subject.name.lower() == name.lower()
                and subject.academic_level_id == academic_level_id
            ):
                raise ValueError(
                    "Subject already exists for this academic level"
                )

        subject = Subject(
            name=name,
            code=code,
            description=description,
            academic_level_id=academic_level_id,
            is_active=True,
        )

        return curriculum.create_subject(
            db,
            subject,
        )

    # =========================
    # Topics
    # =========================

    @staticmethod
    def get_topic(
        db: Session,
        topic_id: int,
    ):
        if topic := curriculum.get_topic(
            db,
            topic_id,
        ):
            return topic
        raise ValueError("Topic not found")

    @staticmethod
    def get_topics_by_subject(
        db: Session,
        subject_id: int,
    ):
        CurriculumService.get_subject(
            db,
            subject_id,
        )

        return curriculum.get_topics_by_subject(
            db,
            subject_id,
        )

    @staticmethod
    def create_topic(
        db: Session,
        subject_id: int,
        name: str,
        description: str | None,
        sequence: int,
    ):
        CurriculumService.get_subject(
            db,
            subject_id,
        )

        topics = curriculum.get_topics_by_subject(
            db,
            subject_id,
        )

        for topic in topics:
            if topic.name.lower() == name.lower():
                raise ValueError(
                    "Topic already exists for this subject"
                )

        topic = Topic(
            subject_id=subject_id,
            name=name,
            description=description,
            sequence=sequence,
            is_active=True,
        )

        return curriculum.create_topic(
            db,
            topic,
        )

    # =========================
    # Lessons
    # =========================

    @staticmethod
    def get_lesson(
        db: Session,
        lesson_id: int,
    ):
        if lesson := curriculum.get_lesson(
            db,
            lesson_id,
        ):
            return lesson
        raise ValueError("Lesson not found")

    @staticmethod
    def get_lessons_by_topic(
        db: Session,
        topic_id: int,
    ):
        CurriculumService.get_topic(
            db,
            topic_id,
        )

        return curriculum.get_lessons_by_topic(
            db,
            topic_id,
        )

    @staticmethod
    def create_lesson(
        db: Session,
        topic_id: int,
        title: str,
        description: str | None,
        content: str | None,
        sequence: int,
        estimated_learning_time: int | None,
    ):
        CurriculumService.get_topic(
            db,
            topic_id,
        )

        lessons = curriculum.get_lessons_by_topic(
            db,
            topic_id,
        )

        for lesson in lessons:
            if lesson.title.lower() == title.lower():
                raise ValueError(
                    "Lesson already exists for this topic"
                )

        lesson = Lesson(
            topic_id=topic_id,
            title=title,
            description=description,
            content=content,
            sequence=sequence,
            estimated_learning_time=estimated_learning_time,
            is_active=True,
        )

        return curriculum.create_lesson(
            db,
            lesson,
        )

    # =========================
    # Learning Objectives
    # =========================

    @staticmethod
    def get_learning_objective(
        db: Session,
        objective_id: int,
    ):
        if objective := curriculum.get_learning_objective(
            db,
            objective_id,
        ):
            return objective
        raise ValueError("Learning objective not found")

    @staticmethod
    def get_objectives_by_lesson(
        db: Session,
        lesson_id: int,
    ):
        CurriculumService.get_lesson(
            db,
            lesson_id,
        )

        return curriculum.get_objectives_by_lesson(
            db,
            lesson_id,
        )

    @staticmethod
    def create_learning_objective(
        db: Session,
        lesson_id: int,
        description: str,
        sequence: int,
    ):
        CurriculumService.get_lesson(
            db,
            lesson_id,
        )

        objectives = curriculum.get_objectives_by_lesson(
            db,
            lesson_id,
        )

        for objective in objectives:
            if (
                objective.description.lower()
                == description.lower()
            ):
                raise ValueError(
                    "Learning objective already exists"
                )

        objective = LearningObjective(
            lesson_id=lesson_id,
            description=description,
            sequence=sequence,
            is_active=True,
        )

        return curriculum.create_learning_objective(
            db,
            objective,
        )