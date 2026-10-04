"""mastery_service.py  (Issue 06)

Turns completed attempts into a persisted learning state, and serves that
state to students (via routes) and to other domains (via the classmethods
below). Pure maths lives in mastery_rules.py; this file is the database shell.

Call chain (Issue 06, section 17)
    Attempt stored -> MasteryService.record_attempt(...) -> topic row (+ objective row)
    -> history row -> state returned. Progress and strength/weakness are derived
    from this stored evidence when read, so they can never go stale.

Public interface for other domains
    record_attempt(db, evidence, commit=True)            -> TopicLearningState
    get_topic_learning_state(db, student_id, topic_id)   -> TopicLearningState
    get_topic_mastery_detail(db, student_id, topic_id)   -> TopicMasteryDetail
    get_student_learning_state(db, student_id)           -> StudentLearningState

Errors: LookupError  -> something referenced does not exist (routes map to 404)
        ValueError   -> the evidence is inconsistent (routes map to 400)

Session note: the project session uses autoflush=False, so every query that
must see pending rows is preceded by an explicit flush().
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.curriculum_ids import LearningObjectiveId, TopicId
from app.models.learning_objective import LearningObjective 
from app.models.lesson import Lesson
from app.models.mastery import Mastery, MasteryHistory, MasteryStatus
from app.models.subject import Subject
from app.models.topic import Topic
from app.models.user import User
from app.schemas.mastery import (
    AttemptEvidence,
    ObjectiveLearningState,
    StudentLearningState,
    TopicLearningState,
    TopicMasteryDetail,
)
from app.services import mastery_rules as rules


def _as_utc(value: datetime) -> datetime:
    return value if value.tzinfo else value.replace(tzinfo=timezone.utc)


class MasteryService:
    # ------------------------------------------------------------------ write
    @staticmethod
    def record_attempt(db: Session, evidence: AttemptEvidence, *, commit: bool = True) -> TopicLearningState:
        """
        Apply one completed attempt to the student's mastery.

        * Topic is derived from the learning objective when one is given, so a
          Mathematics attempt can never touch Biology.
        * Idempotent per attempt_id: reprocessing the same attempt changes nothing.
        * commit=False lets the Attempt domain keep "store attempt + update
          mastery" in one transaction and commit it itself.
        """
        if db.get(User, evidence.student_id) is None:
            raise LookupError("Student not found")

        topic_id, objective_id = MasteryService._resolve_target(db, evidence)
        topic = db.get(Topic, topic_id)
        now = _as_utc(evidence.attempted_at) if evidence.attempted_at else datetime.now(timezone.utc)

        topic_row = MasteryService._get_or_create(db, evidence.student_id, topic_id, None)
        MasteryService._apply_to_row(db, topic_row, evidence, now)

        if objective_id is not None:
            objective_row = MasteryService._get_or_create(db, evidence.student_id, topic_id, objective_id)
            MasteryService._apply_to_row(db, objective_row, evidence, now)

        db.flush()
        state = MasteryService._topic_state(db, topic, topic_row)
        if commit:
            db.commit()
        return state

    @staticmethod
    def _resolve_target(db: Session, evidence: AttemptEvidence) -> tuple[TopicId, LearningObjectiveId | None]:
        """Return (topic_id, learning_objective_id), validating they belong together."""
        if evidence.learning_objective_id is not None:
            row = db.execute(
                select(Lesson.topic_id)
                .join(LearningObjective, LearningObjective.lesson_id == Lesson.id)
                .where(LearningObjective.id == evidence.learning_objective_id)
            ).first()
            if row is None:
                raise LookupError("Learning objective not found")
            if evidence.topic_id is not None and evidence.topic_id != row.topic_id:
                raise ValueError("Learning objective does not belong to the given topic")
            return row.topic_id, evidence.learning_objective_id

        if db.get(Topic, evidence.topic_id) is None:
            raise LookupError("Topic not found")
        return evidence.topic_id, None

    @staticmethod
    def _get_or_create(
        db: Session, student_id: UUID, topic_id: TopicId, objective_id: LearningObjectiveId | None
    ) -> Mastery:
        """Fetch the row locked FOR UPDATE (serialises concurrent attempts), creating it if needed."""
        stmt = select(Mastery).where(Mastery.student_id == student_id, Mastery.topic_id == topic_id)
        if objective_id is None:
            stmt = stmt.where(Mastery.learning_objective_id.is_(None))
        else:
            stmt = stmt.where(Mastery.learning_objective_id == objective_id)

        row = db.execute(stmt.with_for_update()).scalar_one_or_none()
        if row is not None:
            return row

        row = Mastery(
            student_id=student_id,
            topic_id=topic_id,
            learning_objective_id=objective_id,
            mastery_score=rules.INITIAL_SCORE,
            attempts_considered=0,
            correct_attempts=0,
            status=MasteryStatus.BEGINNING,
        )
        try:
            with db.begin_nested():            # a lost race rolls back only this insert
                db.add(row)
                db.flush()
        except IntegrityError:
            row = db.execute(stmt.with_for_update()).scalar_one()
        return row

    @staticmethod
    def _apply_to_row(db: Session, row: Mastery, evidence: AttemptEvidence, now: datetime) -> bool:
        """Update one mastery row. Returns False if this attempt was already counted."""
        already = db.execute(
            select(MasteryHistory.id).where(
                MasteryHistory.mastery_id == row.id,
                MasteryHistory.attempt_ref == evidence.attempt_ref,
            )
        ).first()
        if already is not None:
            return False

        before = row.mastery_score if row.attempts_considered > 0 else rules.INITIAL_SCORE
        after = rules.apply_attempt(before, row.attempts_considered, evidence.score, evidence.difficulty)

        row.mastery_score = after
        row.attempts_considered += 1
        if evidence.is_correct:
            row.correct_attempts += 1
        row.status = rules.classify_status(after, row.attempts_considered)
        if row.last_assessed_at is None or now >= _as_utc(row.last_assessed_at):
            row.last_assessed_at = now

        db.add(
            MasteryHistory(
                mastery_id=row.id,
                attempt_ref=evidence.attempt_ref,
                outcome=evidence.score,
                is_correct=evidence.is_correct,
                difficulty=evidence.difficulty,
                score_before=before,
                score_after=after,
            )
        )
        return True

    # ------------------------------------------------------------------- read
    @staticmethod
    def get_topic_learning_state(db: Session, student_id: UUID, topic_id: TopicId) -> TopicLearningState:
        """The structured answer to "what is this student's current state for this topic?"."""
        topic = db.get(Topic, topic_id)
        if topic is None:
            raise LookupError("Topic not found")
        row = MasteryService._topic_row(db, student_id, topic_id)
        return MasteryService._topic_state(db, topic, row)

    @staticmethod
    def get_topic_mastery_detail(db: Session, student_id: UUID, topic_id: TopicId) -> TopicMasteryDetail:
        """Topic state plus the per-learning-objective breakdown."""
        topic_state = MasteryService.get_topic_learning_state(db, student_id, topic_id)

        pairs = db.execute(
            select(Mastery, LearningObjective)
            .join(LearningObjective, LearningObjective.id == Mastery.learning_objective_id)
            .join(Lesson, Lesson.id == LearningObjective.lesson_id)
            .where(Mastery.student_id == student_id, Mastery.topic_id == topic_id)
            .order_by(Lesson.sequence, LearningObjective.sequence, LearningObjective.description)
        ).all()
        outcomes = MasteryService._recent_outcomes(db, [m.id for m, _ in pairs])

        objectives = [
            ObjectiveLearningState(
                learning_objective_id=objective.id,
                description=objective.description,
                **MasteryService._state_fields(mastery, outcomes.get(mastery.id, [])),
            )
            for mastery, objective in pairs
        ]
        return TopicMasteryDetail(**topic_state.model_dump(), objectives=objectives)

    @staticmethod
    def get_student_learning_state(db: Session, student_id: UUID) -> StudentLearningState:
        """Every active topic the student has evidence for, plus strengths and weaknesses."""
        pairs = db.execute(
            select(Mastery, Topic)
            .join(Topic, Topic.id == Mastery.topic_id)
            .join(Subject, Subject.id == Topic.subject_id)
            .where(
                Mastery.student_id == student_id,
                Mastery.learning_objective_id.is_(None),
                Topic.active.is_(True),
            )
            .order_by(Subject.name, Topic.sequence, Topic.name)
        ).all()
        outcomes = MasteryService._recent_outcomes(db, [m.id for m, _ in pairs])

        topics = [
            TopicLearningState(
                topic_id=topic.id,
                topic_name=topic.name,
                subject_id=topic.subject_id,
                **MasteryService._state_fields(mastery, outcomes.get(mastery.id, [])),
            )
            for mastery, topic in pairs
        ]
        return StudentLearningState(
            topics=topics,
            strengths=sorted((t for t in topics if t.strength), key=lambda t: t.mastery_score, reverse=True),
            weaknesses=sorted((t for t in topics if t.weakness), key=lambda t: t.mastery_score),
        )

    # ---------------------------------------------------------------- helpers
    @staticmethod
    def _topic_row(db: Session, student_id: UUID, topic_id: TopicId) -> Mastery | None:
        return db.execute(
            select(Mastery).where(
                Mastery.student_id == student_id,
                Mastery.topic_id == topic_id,
                Mastery.learning_objective_id.is_(None),
            )
        ).scalar_one_or_none()

    @staticmethod
    def _recent_outcomes(db: Session, mastery_ids: list[int]) -> dict[int, list[float]]:
        """Latest RECENT_OUTCOMES_LIMIT outcomes per mastery row, newest first (one query)."""
        if not mastery_ids:
            return {}
        rank = (
            func.row_number()
            .over(partition_by=MasteryHistory.mastery_id, order_by=MasteryHistory.id.desc())
            .label("rank")
        )
        ranked = (
            select(MasteryHistory.mastery_id.label("mastery_id"), MasteryHistory.outcome.label("outcome"), rank)
            .where(MasteryHistory.mastery_id.in_(mastery_ids))
            .subquery()
        )
        rows = db.execute(
            select(ranked.c.mastery_id, ranked.c.outcome)
            .where(ranked.c.rank <= rules.RECENT_OUTCOMES_LIMIT)
            .order_by(ranked.c.mastery_id, ranked.c.rank)
        ).all()

        result: dict[int, list[float]] = {}
        for mastery_id, outcome in rows:
            result.setdefault(mastery_id, []).append(outcome)
        return result

    @staticmethod
    def _state_fields(row: Mastery | None, outcomes: list[float]) -> dict:
        if row is None:     # no evidence yet: a valid, empty state
            return dict(
                mastery_score=0.0,
                status=MasteryStatus.BEGINNING,
                attempts=0,
                correct_attempts=0,
                incorrect_attempts=0,
                recent_performance=0.0,
                recent_outcomes=[],
                strength=False,
                weakness=False,
                last_assessed_at=None,
            )
        attempts = row.attempts_considered
        return dict(
            mastery_score=round(row.mastery_score, 4),
            status=row.status,
            attempts=attempts,
            correct_attempts=row.correct_attempts,
            incorrect_attempts=attempts - row.correct_attempts,
            recent_performance=round(rules.recent_performance(outcomes), 4),
            recent_outcomes=[round(o, 4) for o in outcomes],
            strength=rules.is_strength(row.mastery_score, attempts),
            weakness=rules.is_weakness(row.mastery_score, attempts),
            last_assessed_at=row.last_assessed_at,
        )

    @staticmethod
    def _topic_state(db: Session, topic: Topic, row: Mastery | None) -> TopicLearningState:
        outcomes = MasteryService._recent_outcomes(db, [row.id]).get(row.id, []) if row else []
        return TopicLearningState(
            topic_id=topic.id,
            topic_name=topic.name,
            subject_id=topic.subject_id,
            **MasteryService._state_fields(row, outcomes),
        )