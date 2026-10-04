"""progress_service.py  (Issue 06)

Progress = how far through the curriculum the student has advanced.
Mastery  = how well they understand it (MasteryService). Different things.

Everything here is computed from stored evidence when asked (lesson
completions + mastery rows), so there is no second copy that could drift.
Only ACTIVE topics and lessons count toward totals; deactivating curriculum
never erases a student's history, it just stops counting toward "how much is left".

A topic is "studied" once the student has completed a lesson in it OR
attempted a question on it.

Academic levels: every topic belongs to one academic level, so "how much of
Mathematics is done" only makes sense for ONE level. get_subject_progress() and
get_overall_progress() therefore accept an optional academic_level_id. Callers
that know the student's level should pass it; with None the totals span every
level that has active topics.

Errors: LookupError -> subject / topic / lesson does not exist (routes -> 404).
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.curriculum_ids import AcademicLevelId, LessonId, SubjectId, TopicId
from app.core.learning_enums import MasteryStatus
from app.models.lesson import Lesson
from app.models.lesson_completion import LessonCompletion
from app.models.mastery import Mastery
from app.models.subject import Subject
from app.models.topic import Topic
from app.schemas.progress import (
    OverallProgress,
    SubjectProgress,
    SubjectProgressSummary,
    TopicProgress,
)
from app.services import mastery_rules as rules


class ProgressService:
    # ------------------------------------------------------------------ write
    @staticmethod
    def mark_lesson_completed(db: Session, student_id: UUID, lesson_id: LessonId, *, commit: bool = True) -> bool:
        """
        Record that the student finished a lesson. Called by the Learning Session
        flow, never exposed to students directly. Returns True if newly recorded,
        False if it was already recorded.
        """
        if db.get(Lesson, lesson_id) is None:
            raise LookupError("Lesson not found")

        exists = db.execute(
            select(LessonCompletion.id).where(
                LessonCompletion.student_id == student_id, LessonCompletion.lesson_id == lesson_id
            )
        ).first()
        if exists is not None:
            return False

        try:
            with db.begin_nested():
                db.add(LessonCompletion(student_id=student_id, lesson_id=lesson_id))
                db.flush()
        except IntegrityError:          # lost a race with a concurrent request: already recorded
            return False
        if commit:
            db.commit()
        return True

    # ------------------------------------------------------------------- read
    @staticmethod
    def get_topic_progress(db: Session, student_id: UUID, topic_id: TopicId) -> TopicProgress:
        topic = db.get(Topic, topic_id)
        if topic is None:
            raise LookupError("Topic not found")
        return ProgressService._topic_progress(db, student_id, [topic])[0]

    @staticmethod
    def get_subject_progress(
        db: Session,
        student_id: UUID,
        subject_id: SubjectId,
        *,
        academic_level_id: AcademicLevelId | None = None,
    ) -> SubjectProgress:
        subject = db.get(Subject, subject_id)
        if subject is None:
            raise LookupError("Subject not found")
        stmt = select(Topic).where(Topic.subject_id == subject_id, Topic.active.is_(True))
        if academic_level_id is not None:
            stmt = stmt.where(Topic.academic_level_id == academic_level_id)
        topics = db.execute(stmt.order_by(Topic.sequence, Topic.name)).scalars().all()
        topic_progress = ProgressService._topic_progress(db, student_id, list(topics))
        summary = ProgressService._summarise(subject, topic_progress)
        return SubjectProgress(**summary.model_dump(), topics=topic_progress)

    @staticmethod
    def get_overall_progress(
        db: Session, student_id: UUID, *, academic_level_id: AcademicLevelId | None = None
    ) -> OverallProgress:
        stmt = select(Topic).where(Topic.active.is_(True))
        if academic_level_id is not None:
            stmt = stmt.where(Topic.academic_level_id == academic_level_id)
        topics = db.execute(stmt.order_by(Topic.sequence, Topic.name)).scalars().all()
        topic_progress = ProgressService._topic_progress(db, student_id, list(topics))

        by_subject: dict[SubjectId, list[TopicProgress]] = {}
        for item in topic_progress:
            by_subject.setdefault(item.subject_id, []).append(item)

        subjects = db.execute(
            select(Subject).where(Subject.id.in_(list(by_subject))).order_by(Subject.name, Subject.id)
        ).scalars().all() if by_subject else []
        summaries = [ProgressService._summarise(s, by_subject[s.id]) for s in subjects]

        totals = ProgressService._totals(topic_progress)
        return OverallProgress(**totals, subjects=summaries)

    # ---------------------------------------------------------------- helpers
    @staticmethod
    def _topic_progress(db: Session, student_id: UUID, topics: list[Topic]) -> list[TopicProgress]:
        """Build progress for many topics with three grouped queries (no N+1)."""
        if not topics:
            return []
        topic_ids = [t.id for t in topics]

        lessons_total = dict(
            db.execute(
                select(Lesson.topic_id, func.count(Lesson.id))
                .where(Lesson.topic_id.in_(topic_ids), Lesson.active.is_(True))
                .group_by(Lesson.topic_id)
            ).all()
        )
        lessons_done = dict(
            db.execute(
                select(Lesson.topic_id, func.count(LessonCompletion.id))
                .join(LessonCompletion, LessonCompletion.lesson_id == Lesson.id)
                .where(
                    LessonCompletion.student_id == student_id,
                    Lesson.topic_id.in_(topic_ids),
                    Lesson.active.is_(True),
                )
                .group_by(Lesson.topic_id)
            ).all()
        )
        mastery_by_topic = {
            m.topic_id: m
            for m in db.execute(
                select(Mastery).where(
                    Mastery.student_id == student_id,
                    Mastery.topic_id.in_(topic_ids),
                    Mastery.learning_objective_id.is_(None),
                )
            ).scalars()
        }

        result = []
        for topic in topics:
            mastery = mastery_by_topic.get(topic.id)
            total = lessons_total.get(topic.id, 0)
            done = lessons_done.get(topic.id, 0)
            attempted = mastery.attempts_considered if mastery else 0
            correct = mastery.correct_attempts if mastery else 0
            score = mastery.mastery_score if mastery else 0.0
            result.append(
                TopicProgress(
                    topic_id=topic.id,
                    topic_name=topic.name,
                    subject_id=topic.subject_id,
                    academic_level_id=topic.academic_level_id,
                    studied=done > 0 or attempted > 0,
                    lessons_total=total,
                    lessons_completed=done,
                    lesson_completion=round(rules.percentage(done, total), 4),
                    questions_attempted=attempted,
                    questions_correct=correct,
                    accuracy=round(rules.percentage(correct, attempted), 4),
                    mastery_score=round(score, 4),
                    status=mastery.status if mastery else MasteryStatus.BEGINNING,
                    strength=rules.is_strength(score, attempted) if mastery else False,
                    weakness=rules.is_weakness(score, attempted) if mastery else False,
                )
            )
        return result

    @staticmethod
    def _totals(items: list[TopicProgress]) -> dict:
        lessons_total = sum(i.lessons_total for i in items)
        lessons_done = sum(i.lessons_completed for i in items)
        attempted = sum(i.questions_attempted for i in items)
        correct = sum(i.questions_correct for i in items)
        scored = [i.mastery_score for i in items if i.questions_attempted > 0]
        return dict(
            topics_total=len(items),
            topics_studied=sum(1 for i in items if i.studied),
            lessons_total=lessons_total,
            lessons_completed=lessons_done,
            completion=round(rules.percentage(lessons_done, lessons_total), 4),
            questions_attempted=attempted,
            questions_correct=correct,
            accuracy=round(rules.percentage(correct, attempted), 4),
            average_mastery=round(sum(scored) / len(scored), 4) if scored else 0.0,
        )

    @staticmethod
    def _summarise(subject: Subject, items: list[TopicProgress]) -> SubjectProgressSummary:
        return SubjectProgressSummary(
            subject_id=subject.id, subject_name=subject.name, **ProgressService._totals(items)
        )