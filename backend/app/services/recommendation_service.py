"""recommendation_service.py  (Issue 08)

Database shell around recommendation_rules.py. It consumes the ADAPTIVE
DECISION (Issue 07) and read-only learning state (Issue 06); it never
recalculates mastery and never re-decides the action.

Call chain (Issue 08, section 16), run by the backend learning flow:

    MasteryService.record_attempt(...)                       # Issue 06
    decision = AdaptiveService.decide_next_action(...)       # Issue 07
    RecommendationService.generate_from_decision(db, student_id, decision)

Public interface
    generate_from_decision(db, student_id, decision, commit=True) -> list[RecommendationOut]
    list_recommendations(db, student_id, ...)                      -> list[RecommendationOut]
    get_recommendation(db, student_id, recommendation_id)          -> RecommendationOut
    update_status(db, student_id, recommendation_id, status)       -> RecommendationOut
    get_teacher_context(db, student_id, topic_id)                  -> TeacherRecommendationContext

Behaviour worth knowing
  * Ownership: every query filters by student_id; a recommendation that belongs
    to someone else is simply "not found".
  * Duplicates: one open (PENDING/ACTIVE) recommendation per (student, topic,
    type). A new decision REFRESHES it in place instead of adding another;
    replaying the same persisted decision is a no-op, even after the student
    dismissed or completed the recommendation.
  * Irrelevance: when a decision for a topic no longer calls for an open
    recommendation about that topic, it is marked SUPERSEDED (kept as history).
  * "Prerequisite" = the preceding active topic in the same subject AND the same
    academic level, by Topic.sequence ("next topic" likewise). Topics at other
    levels are never suggested. The curriculum has no prerequisite graph yet;
    when it does, replace _previous_topic() / _next_topic() and nothing else changes.

Errors: LookupError -> student / topic / recommendation not found (routes -> 404)
        InvalidStatusTransition -> status change not allowed (routes -> 409)
        ValueError -> inconsistent input, e.g. a decision from another student (routes -> 400)
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import case, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.curriculum_ids import SubjectId, TopicId
from app.core.learning_enums import (
    AdaptiveAction,
    RecommendationPriority,
    RecommendationStatus,
)
from app.models.adaptive_decision import AdaptiveDecision
from app.models.recommendation import Recommendation
from app.models.subject import Subject
from app.models.topic import Topic
from app.models.user import User
from app.schemas.adaptive import AdaptiveDecisionOut
from app.schemas.recommendation import RecommendationOut, TeacherRecommendationContext
from app.services import recommendation_rules as rules
from app.services.mastery_service import MasteryService


class InvalidStatusTransition(ValueError):
    """The requested status change is not allowed from the current status."""


_PRIORITY_ORDER = case(
    (Recommendation.priority == RecommendationPriority.HIGH, 1),
    (Recommendation.priority == RecommendationPriority.MEDIUM, 2),
    else_=3,
)


class RecommendationService:
    # --------------------------------------------------------------- generate
    @staticmethod
    def generate_from_decision(
        db: Session,
        student_id: UUID,
        decision: AdaptiveDecisionOut,
        *,
        commit: bool = True,
        config: rules.RecommendationConfig = rules.DEFAULT_CONFIG,
    ) -> list[RecommendationOut]:
        """Turn one adaptive decision into stored recommendations (most urgent first)."""
        if db.get(User, student_id) is None:
            raise LookupError("Student not found")
        topic = db.get(Topic, decision.topic_id)
        if topic is None:
            raise LookupError("Topic not found")
        subject = db.get(Subject, topic.subject_id)

        if decision.decision_id is not None:
            record = db.get(AdaptiveDecision, decision.decision_id)
            if record is None or record.student_id != student_id or record.topic_id != topic.id:
                raise ValueError("Adaptive decision does not belong to this student and topic")
            already = RecommendationService._ids_for_decision(db, student_id, decision.decision_id)
            if already:                                    # replay: nothing to do
                return RecommendationService._fetch(db, student_id, already)

        prerequisite = None
        if decision.action in config.prerequisite_checked_actions:
            previous = RecommendationService._previous_topic(db, topic)
            if previous is not None:
                # Read-only: we reuse the mastery domain's status, we do not recompute it.
                state = MasteryService.get_topic_learning_state(db, student_id, previous.id)
                prerequisite = rules.PrerequisiteState(
                    topic=rules.TopicRef(previous.id, previous.name),
                    status=state.status,
                    attempts=state.attempts,
                )

        next_topic = None
        if decision.action == AdaptiveAction.PROGRESS:
            following = RecommendationService._next_topic(db, topic)
            if following is not None:
                next_topic = rules.TopicRef(following.id, following.name)

        drafts = rules.plan_recommendations(
            rules.DecisionContext(
                action=decision.action,
                topic=rules.TopicRef(topic.id, topic.name),
                subject_name=subject.name,
                difficulty=decision.difficulty,
                reason_code=decision.reason_code,
                reason=decision.reason,
            ),
            prerequisite,
            next_topic,
            config,
        )

        kept_ids = [
            RecommendationService._upsert_open(db, student_id, subject.id, draft, decision.decision_id).id
            for draft in drafts
        ]

        # Open recommendations about this topic that the new decision no longer calls for.
        stale = db.execute(
            select(Recommendation).where(
                Recommendation.student_id == student_id,
                Recommendation.status.in_(rules.OPEN_STATUSES),
                or_(Recommendation.topic_id == topic.id, Recommendation.related_topic_id == topic.id),
                Recommendation.id.not_in(kept_ids),
            )
        ).scalars().all()
        for row in stale:
            row.status = RecommendationStatus.SUPERSEDED

        db.flush()
        result = RecommendationService._fetch(db, student_id, kept_ids)
        if commit:
            db.commit()
        return result

    @staticmethod
    def _upsert_open(
        db: Session, student_id: UUID, subject_id: SubjectId, draft: rules.RecommendationDraft, decision_id: int | None
    ) -> Recommendation:
        """Refresh the open recommendation for (type, topic) or create one."""

        def refresh(row: Recommendation) -> Recommendation:
            row.action = draft.action
            row.reason = draft.reason
            row.reason_code = draft.reason_code
            row.priority = draft.priority
            row.difficulty = draft.difficulty
            row.related_topic_id = draft.related_topic_id
            row.adaptive_decision_id = decision_id
            return row                      # status untouched: an ACTIVE one stays ACTIVE

        existing = RecommendationService._open_row(db, student_id, draft)
        if existing is not None:
            return refresh(existing)

        row = Recommendation(
            student_id=student_id,
            subject_id=subject_id,
            topic_id=draft.topic_id,
            related_topic_id=draft.related_topic_id,
            adaptive_decision_id=decision_id,
            type=draft.type,
            action=draft.action,
            reason=draft.reason,
            reason_code=draft.reason_code,
            priority=draft.priority,
            difficulty=draft.difficulty,
            status=RecommendationStatus.PENDING,
        )
        try:
            with db.begin_nested():         # a lost race rolls back only this insert
                db.add(row)
                db.flush()
        except IntegrityError:
            return refresh(RecommendationService._open_row(db, student_id, draft))
        return row

    @staticmethod
    def _open_row(db: Session, student_id: UUID, draft: rules.RecommendationDraft) -> Recommendation | None:
        return db.execute(
            select(Recommendation)
            .where(
                Recommendation.student_id == student_id,
                Recommendation.topic_id == draft.topic_id,
                Recommendation.type == draft.type,
                Recommendation.status.in_(rules.OPEN_STATUSES),
            )
            .with_for_update()
        ).scalar_one_or_none()

    @staticmethod
    def _ids_for_decision(db: Session, student_id: UUID, decision_id: int) -> list[int]:
        return list(
            db.execute(
                select(Recommendation.id).where(
                    Recommendation.student_id == student_id,
                    Recommendation.adaptive_decision_id == decision_id,
                )
            ).scalars()
        )

    # ------------------------------------------------------------- curriculum
    @staticmethod
    def _previous_topic(db: Session, topic: Topic) -> Topic | None:
        """The 'prerequisite': preceding active topic of the same subject AND academic level."""
        return db.execute(
            select(Topic)
            .where(
                Topic.subject_id == topic.subject_id,
                Topic.academic_level_id == topic.academic_level_id,
                Topic.active.is_(True),
                Topic.sequence < topic.sequence,
            )
            .order_by(Topic.sequence.desc(), Topic.name)
            .limit(1)
        ).scalar_one_or_none()

    @staticmethod
    def _next_topic(db: Session, topic: Topic) -> Topic | None:
        """The following active topic of the same subject AND academic level."""
        return db.execute(
            select(Topic)
            .where(
                Topic.subject_id == topic.subject_id,
                Topic.academic_level_id == topic.academic_level_id,
                Topic.active.is_(True),
                Topic.sequence > topic.sequence,
            )
            .order_by(Topic.sequence, Topic.name)
            .limit(1)
        ).scalar_one_or_none()

    # --------------------------------------------------------------- retrieve
    @staticmethod
    def list_recommendations(
        db: Session,
        student_id: UUID,
        *,
        statuses: list[RecommendationStatus] | None = None,
        topic_id: TopicId | None = None,
        subject_id: SubjectId | None = None,
        include_history: bool = False,
        limit: int = 100,
    ) -> list[RecommendationOut]:
        """
        Default: the student's CURRENT (open) recommendations, most urgent first.
        include_history=True (or explicit statuses): everything matching, newest first.
        """
        stmt = RecommendationService._base_query(student_id)
        if statuses:
            stmt = stmt.where(Recommendation.status.in_(statuses))
        elif not include_history:
            stmt = stmt.where(Recommendation.status.in_(rules.OPEN_STATUSES))
        if topic_id is not None:
            stmt = stmt.where(Recommendation.topic_id == topic_id)
        if subject_id is not None:
            stmt = stmt.where(Recommendation.subject_id == subject_id)

        if statuses or include_history:
            stmt = stmt.order_by(Recommendation.id.desc())
        else:
            stmt = stmt.order_by(_PRIORITY_ORDER, Recommendation.id.desc())
        return RecommendationService._to_out(db.execute(stmt.limit(limit)).all())

    @staticmethod
    def get_recommendation(db: Session, student_id: UUID, recommendation_id: int) -> RecommendationOut:
        rows = db.execute(
            RecommendationService._base_query(student_id).where(Recommendation.id == recommendation_id)
        ).all()
        if not rows:                         # not found OR someone else's: indistinguishable on purpose
            raise LookupError("Recommendation not found")
        return RecommendationService._to_out(rows)[0]

    @staticmethod
    def update_status(
        db: Session,
        student_id: UUID,
        recommendation_id: int,
        new_status: RecommendationStatus,
        *,
        commit: bool = True,
    ) -> RecommendationOut:
        row = db.execute(
            select(Recommendation)
            .where(Recommendation.id == recommendation_id, Recommendation.student_id == student_id)
            .with_for_update()
        ).scalar_one_or_none()
        if row is None:
            raise LookupError("Recommendation not found")
        if new_status not in rules.STUDENT_SETTABLE:
            raise ValueError(f"Students cannot set status {new_status.value}")
        if not rules.can_transition(row.status, new_status):
            raise InvalidStatusTransition(
                f"Cannot change a {row.status.value} recommendation to {new_status.value}"
            )
        row.status = new_status
        db.flush()
        if commit:
            db.commit()
        return RecommendationService.get_recommendation(db, student_id, recommendation_id)

    @staticmethod
    def get_teacher_context(
        db: Session, student_id: UUID, topic_id: TopicId, *, history_limit: int = 5
    ) -> TeacherRecommendationContext:
        """
        Structured recommendations for the AI orchestration layer / context builder.
        Relevant = about this topic, or triggered by it (e.g. 'review the prerequisite',
        'advance to the next topic'). `primary` is the plan the Artificial Teacher
        should align with rather than invent a conflicting one.
        """
        if db.get(Topic, topic_id) is None:
            raise LookupError("Topic not found")
        relevant = or_(Recommendation.topic_id == topic_id, Recommendation.related_topic_id == topic_id)
        base = RecommendationService._base_query(student_id).where(relevant)

        open_rows = db.execute(
            base.where(Recommendation.status.in_(rules.OPEN_STATUSES)).order_by(_PRIORITY_ORDER, Recommendation.id.desc())
        ).all()
        history_rows = db.execute(
            base.where(Recommendation.status.not_in(rules.OPEN_STATUSES))
            .order_by(Recommendation.id.desc())
            .limit(history_limit)
        ).all()

        open_items = RecommendationService._to_out(open_rows)
        return TeacherRecommendationContext(
            topic_id=topic_id,
            primary=open_items[0] if open_items else None,
            open=open_items,
            recent_history=RecommendationService._to_out(history_rows),
        )

    # ---------------------------------------------------------------- helpers
    @staticmethod
    def _base_query(student_id: UUID):
        return (
            select(Recommendation, Topic.name, Subject.name)
            .join(Topic, Topic.id == Recommendation.topic_id)
            .join(Subject, Subject.id == Recommendation.subject_id)
            .where(Recommendation.student_id == student_id)
        )

    @staticmethod
    def _fetch(db: Session, student_id: UUID, ids: list[int]) -> list[RecommendationOut]:
        if not ids:
            return []
        rows = db.execute(
            RecommendationService._base_query(student_id)
            .where(Recommendation.id.in_(ids))
            .order_by(_PRIORITY_ORDER, Recommendation.id)
        ).all()
        return RecommendationService._to_out(rows)

    @staticmethod
    def _to_out(rows) -> list[RecommendationOut]:
        return [
            RecommendationOut(
                id=rec.id,
                subject_id=rec.subject_id,
                subject_name=subject_name,
                topic_id=rec.topic_id,
                topic_name=topic_name,
                related_topic_id=rec.related_topic_id,
                type=rec.type,
                action=rec.action,
                reason=rec.reason,
                reason_code=rec.reason_code,
                priority=rec.priority,
                difficulty=rec.difficulty,
                status=rec.status,
                adaptive_decision_id=rec.adaptive_decision_id,
                created_at=rec.created_at,
                updated_at=rec.updated_at,
            )
            for rec, topic_name, subject_name in rows
        ]
