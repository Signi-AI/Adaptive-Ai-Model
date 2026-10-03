"""adaptive_service.py  (Issue 07)

Gathers one student's learning state for one topic through the Issue 06
service interfaces (never by reading mastery/attempt tables directly), runs
the pure rules in adaptive_rules.py, optionally records the decision, and
returns a structured AdaptiveDecisionOut.

It does NOT generate questions, lessons, mastery, progress, recommendations or
teaching text. Consumers act on the decision:

    PRACTICE/ASSESS + difficulty -> Question Service
    reason_code / reason + state -> Recommendation Service
    action + topic + reason      -> Artificial Teacher Service

Typical use (inside the learning flow, after mastery has been updated):

    decision = AdaptiveService.decide_next_action(db, student_id, topic_id, session_id)

Call it once per learning step: a persisted TEACH/REVISE decision is followed by
PRACTICE on the next call when no new answer has arrived (see adaptive_rules).
Use persist=False for a side-effect-free preview.

Errors: LookupError -> topic not found (routes map to 404).
"""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.learning_enums import ReasonCode, Trend
from app.models.adaptive_decision import AdaptiveDecision
from app.schemas.adaptive import AdaptiveDecisionOut
from app.services.adaptive_rules import AdaptiveInput, RuleDecision, decide
from app.services.mastery_service import MasteryService
from app.services.progress_service import ProgressService


class AdaptiveService:
    @staticmethod
    def decide_next_action(
        db: Session,
        student_id: UUID,
        topic_id: int,
        session_id: str | None = None,
        *,
        persist: bool = True,
        commit: bool = True,
    ) -> AdaptiveDecisionOut:
        # Learning state comes from the Issue 06 domain interfaces only.
        state = MasteryService.get_topic_learning_state(db, student_id, topic_id)   # LookupError if no topic
        progress = ProgressService.get_topic_progress(db, student_id, topic_id)
        previous = AdaptiveService._latest_row(db, student_id, topic_id)

        result = decide(
            AdaptiveInput(
                topic_id=topic_id,
                mastery_score=state.mastery_score,
                attempts=state.attempts,
                recent_outcomes=tuple(state.recent_outcomes),
                lessons_completed=progress.lessons_completed,
                lessons_total=progress.lessons_total,
                previous_action=previous.action if previous else None,
                previous_difficulty=previous.difficulty if previous else None,
                attempts_at_previous_decision=previous.attempts_at_decision if previous else None,
            )
        )

        decision_id, decided_at = None, datetime.now(timezone.utc)
        if persist:
            record = AdaptiveDecision(
                student_id=student_id,
                topic_id=topic_id,
                session_id=session_id,
                action=result.action,
                difficulty=result.difficulty,
                reason_code=result.reason_code.value,
                reason=result.reason,
                mastery_score=state.mastery_score,
                recent_performance=result.recent_performance,
                attempts_at_decision=state.attempts,
            )
            db.add(record)
            db.flush()
            decision_id, decided_at = record.id, record.created_at
            if commit:
                db.commit()

        return AdaptiveService._to_out(
            result, topic_id, state.mastery_score, state.attempts, session_id, decision_id, decided_at
        )

    @staticmethod
    def get_latest_decision(db: Session, student_id: UUID, topic_id: int) -> AdaptiveDecisionOut | None:
        """The most recent stored decision for this student and topic, if any."""
        row = AdaptiveService._latest_row(db, student_id, topic_id)
        if row is None:
            return None
        return AdaptiveDecisionOut(
            decision_id=row.id,
            action=row.action,
            topic_id=row.topic_id,
            difficulty=row.difficulty,
            reason_code=ReasonCode(row.reason_code),
            reason=row.reason,
            mastery_score=row.mastery_score,
            recent_performance=row.recent_performance,
            trend=Trend.UNKNOWN,            # trend is not stored; recompute via decide_next_action(persist=False)
            attempts=row.attempts_at_decision,
            session_id=row.session_id,
            decided_at=row.created_at,
        )

    # ---------------------------------------------------------------- helpers
    @staticmethod
    def _latest_row(db: Session, student_id: UUID, topic_id: int) -> AdaptiveDecision | None:
        return db.execute(
            select(AdaptiveDecision)
            .where(AdaptiveDecision.student_id == student_id, AdaptiveDecision.topic_id == topic_id)
            .order_by(AdaptiveDecision.id.desc())
            .limit(1)
        ).scalar_one_or_none()

    @staticmethod
    def _to_out(
        result: RuleDecision,
        topic_id: int,
        mastery_score: float,
        attempts: int,
        session_id: str | None,
        decision_id: int | None,
        decided_at: datetime,
    ) -> AdaptiveDecisionOut:
        return AdaptiveDecisionOut(
            decision_id=decision_id,
            action=result.action,
            topic_id=topic_id,
            difficulty=result.difficulty,
            reason_code=result.reason_code,
            reason=result.reason,
            mastery_score=mastery_score,
            recent_performance=round(result.recent_performance, 4),
            trend=result.trend,
            attempts=attempts,
            session_id=session_id,
            decided_at=decided_at,
        )