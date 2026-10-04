"""recommendation_rules.py  (Issue 08)

Pure rules: turn an ADAPTIVE DECISION into concrete, student-facing
recommendations. No database, no FastAPI, no SQLAlchemy -- standard library
only -- so the whole mapping is unit-testable and every wording/priority choice
lives in one place.

This module never recalculates mastery and never re-decides the action. It
trusts the adaptive decision (Issue 07) and the learning state it is handed
(Issue 06) and only answers: "what concrete action do we recommend?"

Mapping
-------
  adaptive action   recommendation                                   priority
  ---------------   ---------------------------------------------   --------
  TEACH             CONTINUE  start the topic's lessons               MEDIUM
  REVISE            REMEDIATE re-learn the topic + easy practice      HIGH
  PRACTICE          PRACTICE  exercises at the decided difficulty     MEDIUM
                              (HIGH when the adaptive reason is a performance drop)
  ASSESS            PRACTICE  a more demanding "prove it" set         LOW
  PROGRESS          ADVANCE   move to the next topic                  MEDIUM

Prerequisite protection (TEACH and REVISE only)
-----------------------------------------------
If the preceding topic has solid evidence of being shaky, the student is sent
back to it FIRST (REVIEW, HIGH):
  * REVISE  -> REVIEW(prerequisite, HIGH) + REMEDIATE(topic, MEDIUM, "after reviewing...")
  * TEACH   -> REVIEW(prerequisite, HIGH) only. We do not recommend starting new
               material while the foundation underneath it is still struggling.
A prerequisite with too little evidence is never called weak: no guessing.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.core.curriculum_ids import TopicId
from app.core.learning_enums import (
    AdaptiveAction,
    Difficulty,
    MasteryStatus,
    RecommendationPriority,
    RecommendationStatus,
    RecommendationType,
    ReasonCode,
)

# --------------------------------------------------------------------------
# Configuration (all tunable choices in one place)
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class RecommendationConfig:
    # A prerequisite is "shaky" when it has at least this many attempts AND its
    # mastery status is not one of the OK statuses. (Status comes from the
    # mastery domain as-is; nothing is recalculated here.)
    prerequisite_min_attempts: int = 3
    prerequisite_ok_statuses: tuple[MasteryStatus, ...] = (MasteryStatus.PROFICIENT, MasteryStatus.MASTERED)
    prerequisite_checked_actions: tuple[AdaptiveAction, ...] = (AdaptiveAction.TEACH, AdaptiveAction.REVISE)

    default_practice_difficulty: Difficulty = Difficulty.MEDIUM


DEFAULT_CONFIG = RecommendationConfig()


# --------------------------------------------------------------------------
# Input / output
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class TopicRef:
    topic_id: TopicId
    name: str


@dataclass(frozen=True)
class DecisionContext:
    """The adaptive decision, plus the names needed to word the recommendation."""

    action: AdaptiveAction
    topic: TopicRef
    subject_name: str
    difficulty: Difficulty | None
    reason_code: ReasonCode | str
    reason: str


@dataclass(frozen=True)
class PrerequisiteState:
    """Read-only snapshot of the preceding topic, taken from the mastery domain."""

    topic: TopicRef
    status: MasteryStatus
    attempts: int


@dataclass(frozen=True)
class RecommendationDraft:
    type: RecommendationType
    topic_id: TopicId                   # the topic the student should study
    related_topic_id: TopicId | None    # the topic whose decision triggered this (if different)
    action: str                         # what to do, in plain words
    reason: str                         # why
    reason_code: str
    priority: RecommendationPriority
    difficulty: Difficulty | None = None

    @property
    def key(self) -> tuple[RecommendationType, TopicId]:
        """Identity used to avoid duplicates: one open recommendation per (type, topic)."""
        return (self.type, self.topic_id)


# --------------------------------------------------------------------------
# Rules
# --------------------------------------------------------------------------
def is_prerequisite_blocking(
    prerequisite: PrerequisiteState | None, config: RecommendationConfig = DEFAULT_CONFIG
) -> bool:
    """True only with real evidence that the foundation topic is not solid yet."""
    if prerequisite is None:
        return False
    return (
        prerequisite.attempts >= config.prerequisite_min_attempts
        and prerequisite.status not in config.prerequisite_ok_statuses
    )


def _code(decision: DecisionContext) -> str:
    return decision.reason_code.value if isinstance(decision.reason_code, ReasonCode) else str(decision.reason_code)


def _level(difficulty: Difficulty | None, config: RecommendationConfig) -> str:
    return (difficulty or config.default_practice_difficulty).value.lower()


def plan_recommendations(
    decision: DecisionContext,
    prerequisite: PrerequisiteState | None = None,
    next_topic: TopicRef | None = None,
    config: RecommendationConfig = DEFAULT_CONFIG,
) -> list[RecommendationDraft]:
    """Return the recommendations for one adaptive decision, most urgent first."""
    topic = decision.topic
    blocking = (
        decision.action in config.prerequisite_checked_actions
        and is_prerequisite_blocking(prerequisite, config)
    )
    drafts: list[RecommendationDraft] = []

    # --- a shaky foundation comes first -----------------------------------
    if blocking:
        assert prerequisite is not None
        if decision.action == AdaptiveAction.REVISE:
            why = (
                f"You are struggling with {topic.name}, and your results in "
                f"{prerequisite.topic.name} show the basics need strengthening first."
            )
            text = f"Review {prerequisite.topic.name} first -- {topic.name} builds on it."
        else:
            why = (
                f"Your results in {prerequisite.topic.name} show it is not yet secure, "
                f"so review it before starting {topic.name}."
            )
            text = f"Review {prerequisite.topic.name} before starting {topic.name}."
        drafts.append(
            RecommendationDraft(
                type=RecommendationType.REVIEW,
                topic_id=prerequisite.topic.topic_id,
                related_topic_id=topic.topic_id,
                action=text,
                reason=why,
                reason_code="PREREQUISITE_NOT_SECURE",
                priority=RecommendationPriority.HIGH,
            )
        )

    # --- the recommendation for the decision's own topic ------------------
    code = _code(decision)

    if decision.action == AdaptiveAction.TEACH:
        if not blocking:                       # never recommend new material over a weak foundation
            drafts.append(
                RecommendationDraft(
                    type=RecommendationType.CONTINUE,
                    topic_id=topic.topic_id,
                    related_topic_id=None,
                    action=f"Start the {topic.name} lesson and work through its examples.",
                    reason=decision.reason,
                    reason_code=code,
                    priority=RecommendationPriority.MEDIUM,
                )
            )

    elif decision.action == AdaptiveAction.REVISE:
        text = (
            f"After reviewing {prerequisite.topic.name}, go back to the {topic.name} lesson "
            "and complete easy guided practice questions."
            if blocking
            else f"Review the {topic.name} lesson, then complete easy guided practice questions."
        )
        drafts.append(
            RecommendationDraft(
                type=RecommendationType.REMEDIATE,
                topic_id=topic.topic_id,
                related_topic_id=None,
                action=text,
                reason=decision.reason,
                reason_code=code,
                priority=RecommendationPriority.MEDIUM if blocking else RecommendationPriority.HIGH,
                difficulty=Difficulty.EASY,
            )
        )

    elif decision.action == AdaptiveAction.PRACTICE:
        dropped = code == ReasonCode.PERFORMANCE_DROP.value
        drafts.append(
            RecommendationDraft(
                type=RecommendationType.PRACTICE,
                topic_id=topic.topic_id,
                related_topic_id=None,
                action=f"Complete {_level(decision.difficulty, config)}-level practice exercises on {topic.name}.",
                reason=decision.reason,
                reason_code=code,
                priority=RecommendationPriority.HIGH if dropped else RecommendationPriority.MEDIUM,
                difficulty=decision.difficulty or config.default_practice_difficulty,
            )
        )

    elif decision.action == AdaptiveAction.ASSESS:
        drafts.append(
            RecommendationDraft(
                type=RecommendationType.PRACTICE,
                topic_id=topic.topic_id,
                related_topic_id=None,
                action=(
                    f"Challenge yourself with {_level(decision.difficulty, config)}-level questions "
                    f"on {topic.name} to confirm you have mastered it."
                ),
                reason=decision.reason,
                reason_code=code,
                priority=RecommendationPriority.LOW,
                difficulty=decision.difficulty or config.default_practice_difficulty,
            )
        )

    elif decision.action == AdaptiveAction.PROGRESS:
        if next_topic is not None:
            drafts.append(
                RecommendationDraft(
                    type=RecommendationType.ADVANCE,
                    topic_id=next_topic.topic_id,
                    related_topic_id=topic.topic_id,
                    action=f"You have mastered {topic.name}. Move on to {next_topic.name}.",
                    reason=decision.reason,
                    reason_code=code,
                    priority=RecommendationPriority.MEDIUM,
                )
            )
        else:
            drafts.append(
                RecommendationDraft(
                    type=RecommendationType.ADVANCE,
                    topic_id=topic.topic_id,
                    related_topic_id=None,
                    action=(
                        f"You have mastered {topic.name}, the last {decision.subject_name} topic at this level. "
                        "Choose another subject to keep progressing."
                    ),
                    reason=decision.reason,
                    reason_code=code,
                    priority=RecommendationPriority.MEDIUM,
                )
            )

    return sorted(drafts, key=lambda d: priority_rank(d.priority))


# --------------------------------------------------------------------------
# Priority and status rules
# --------------------------------------------------------------------------
_PRIORITY_RANK = {
    RecommendationPriority.HIGH: 1,
    RecommendationPriority.MEDIUM: 2,
    RecommendationPriority.LOW: 3,
}


def priority_rank(priority: RecommendationPriority) -> int:
    """Sort key: smaller = more urgent."""
    return _PRIORITY_RANK[priority]


OPEN_STATUSES = (RecommendationStatus.PENDING, RecommendationStatus.ACTIVE)

# What a STUDENT may set through the API. SUPERSEDED is reserved for the system.
STUDENT_SETTABLE = (
    RecommendationStatus.ACTIVE,
    RecommendationStatus.COMPLETED,
    RecommendationStatus.DISMISSED,
)

_TRANSITIONS = {
    RecommendationStatus.PENDING: {
        RecommendationStatus.ACTIVE,
        RecommendationStatus.COMPLETED,
        RecommendationStatus.DISMISSED,
        RecommendationStatus.SUPERSEDED,
    },
    RecommendationStatus.ACTIVE: {
        RecommendationStatus.COMPLETED,
        RecommendationStatus.DISMISSED,
        RecommendationStatus.SUPERSEDED,
    },
    RecommendationStatus.COMPLETED: set(),
    RecommendationStatus.DISMISSED: set(),
    RecommendationStatus.SUPERSEDED: set(),
}


def is_open(status: RecommendationStatus) -> bool:
    return status in OPEN_STATUSES


def can_transition(current: RecommendationStatus, target: RecommendationStatus) -> bool:
    """Closed states are final. Repeating the current status is a harmless no-op."""
    return current == target or target in _TRANSITIONS[current]
