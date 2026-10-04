"""core/curriculum_ids.py

The ONE place that says what type curriculum primary keys are
(Subject, Topic, Lesson, LearningObjective, AcademicLevel).

They are UUIDs. If any of them ever changes type, change the aliases below and
id_column_type(); the models, schemas, services and routes of the mastery /
adaptive / recommendation domains all take their id types from here.

Standard library only at import time (SQLAlchemy is imported lazily inside
id_column_type) so the pure rule modules can import the aliases freely.
"""

import uuid

SubjectId = uuid.UUID
TopicId = uuid.UUID
LessonId = uuid.UUID
LearningObjectiveId = uuid.UUID
AcademicLevelId = uuid.UUID


def id_column_type():
    """SQLAlchemy column type for a foreign key pointing at a curriculum table."""
    from sqlalchemy import UUID

    return UUID(as_uuid=True)
