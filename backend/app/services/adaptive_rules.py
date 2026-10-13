"""adaptive_rules.py  (Issue 07)

The adaptive decision logic as pure functions: no database, no FastAPI, no
SQLAlchemy -- only the standard library. adaptive_service.py gathers the
learning state and calls decide(); everything about *what to do next* lives
here and every threshold lives in AdaptiveConfig.

Question answered: "given what we know about this student on THIS topic,
what should happen next?"  Nothing here generates a question, a lesson, a
mastery score or a recommendation -- it only picks (action, difficulty, why).

Rule order (first match wins)
-----------------------------
1. Follow-up   Last decision was TEACH/REVISE and no new attempt has arrived
               since -> PRACTICE (EASY). Without this a weak student would be
               told to REVISE forever, because teaching alone adds no evidence.
2. No evidence No attempts yet -> TEACH (nothing taught) / PRACTICE (lessons
               done, no questions yet), at the starting difficulty.
3. Thin data   Fewer than min_attempts_to_adapt attempts -> PRACTICE at the
               previous (or starting) difficulty. One or two answers never
               trigger remediation or escalation.
4. Evidence    a. REVISE   low mastery AND poor recent performance
               b. PROGRESS mastered, enough attempts, strong AND consistent
               c. ASSESS   proficient mastery + strong recent performance but
                           not (yet) proven -> a more demanding check
               d. PRACTICE everything else; difficulty moves at most ONE level
                           per decision, from the previous difficulty (or the
                           mastery-based baseline on first contact)
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from app.core.curriculum_ids import TopicId
from app.core.learning_enums import AdaptiveAction, Difficulty, ReasonCode, Trend
from app.services import mastery_rules as mr


# --------------------------------------------------------------------------
# Centralised, tunable thresholds
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class AdaptiveConfig:
    # Mastery bands. Default to the Issue 06 status boundaries so the two
    # domains agree on what "low" / "proficient" / "mastered" mean; override
    # here to tune the adaptive engine without touching mastery.
    low_mastery_threshold: float = mr.DEVELOPING_MIN               # 0.40
    proficient_mastery_threshold: float = mr.PROFICIENT_MIN        # 0.70
    progress_mastery_threshold: float = mr.MASTERED_MIN            # 0.85

    # Recent performance (mean outcome of the last RECENT_WINDOW attempts).
    poor_performance_threshold: float = 0.40
    strong_performance_threshold: float = 0.80
    difficulty_decrease_threshold: float = 0.50
    difficulty_increase_threshold: float = 0.80

    # Evidence required before the engine reacts at all.
    min_attempts_to_adapt: int = 3
    min_attempts_to_progress: int = mr.MIN_ATTEMPTS_FOR_MASTERED   # 5

    # "Consistent" = none of the latest N outcomes is a failure.
    consistency_window: int = 3
    consistency_min_outcome: float = 0.5

    # Trend = mean(latest window) - mean(window before it).
    trend_window: int = mr.RECENT_WINDOW
    trend_min_earlier: int = 3
    trend_delta: float = 0.15

    # Baseline difficulty by mastery, used when there is no previous decision.
    medium_difficulty_min_mastery: float = 0.40
    hard_difficulty_min_mastery: float = 0.70

    starting_difficulty: Difficulty = Difficulty.EASY
    follow_up_difficulty: Difficulty = Difficulty.EASY


DEFAULT_CONFIG = AdaptiveConfig()

_DIFFICULTY_ORDER = (Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD)


# --------------------------------------------------------------------------
# Input / output
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class AdaptiveInput:
    """Everything the rules need, for ONE student on ONE topic."""

    topic_id: TopicId
    mastery_score: float
    attempts: int
    recent_outcomes: Sequence[float] = ()      # newest first
    lessons_completed: int = 0
    lessons_total: int = 0
    previous_action: AdaptiveAction | None = None
    previous_difficulty: Difficulty | None = None
    attempts_at_previous_decision: int | None = None


@dataclass(frozen=True)
class RuleDecision:
    action: AdaptiveAction
    difficulty: Difficulty | None      # None for PROGRESS (nothing to be asked)
    reason_code: ReasonCode
    reason: str
    trend: Trend
    recent_performance: float


# --------------------------------------------------------------------------
# Building blocks
# --------------------------------------------------------------------------
def step_difficulty(level: Difficulty, delta: int) -> Difficulty:
    """Move up/down the EASY-MEDIUM-HARD ladder, clamped at both ends."""
    index = _DIFFICULTY_ORDER.index(level) + delta
    return _DIFFICULTY_ORDER[max(0, min(len(_DIFFICULTY_ORDER) - 1, index))]


def baseline_difficulty(mastery_score: float, config: AdaptiveConfig = DEFAULT_CONFIG) -> Difficulty:
    if mastery_score < config.medium_difficulty_min_mastery:
        return Difficulty.EASY
    if mastery_score < config.hard_difficulty_min_mastery:
        return Difficulty.MEDIUM
    return Difficulty.HARD


def compute_trend(outcomes: Sequence[float], config: AdaptiveConfig = DEFAULT_CONFIG) -> Trend:
    """Compare the latest window with the window before it (outcomes newest first)."""
    latest = list(outcomes[: config.trend_window])
    earlier = list(outcomes[config.trend_window : 2 * config.trend_window])
    if len(latest) < config.trend_window or len(earlier) < config.trend_min_earlier:
        return Trend.UNKNOWN
    delta = sum(latest) / len(latest) - sum(earlier) / len(earlier)
    if delta >= config.trend_delta:
        return Trend.IMPROVING
    if delta <= -config.trend_delta:
        return Trend.DECLINING
    return Trend.STABLE


def is_consistent(outcomes: Sequence[float], config: AdaptiveConfig = DEFAULT_CONFIG) -> bool:
    """True when none of the latest few outcomes is a failure."""
    window = list(outcomes[: config.consistency_window])
    return bool(window) and all(o >= config.consistency_min_outcome for o in window)


def select_practice_difficulty(
    mastery_score: float,
    performance: float,
    trend: Trend,
    consistent: bool,
    previous: Difficulty | None,
    config: AdaptiveConfig = DEFAULT_CONFIG,
) -> Difficulty:
    """
    Anchor on the previous difficulty (stability) or the mastery baseline, then
    move at most one level:
      * poor recent performance (and not already recovering)  -> one easier
      * strong, consistent performance (and not declining)    -> one harder
      * otherwise                                             -> unchanged
    """
    anchor = previous or baseline_difficulty(mastery_score, config)
    if performance < config.difficulty_decrease_threshold and trend != Trend.IMPROVING:
        return step_difficulty(anchor, -1)
    if (
        performance >= config.difficulty_increase_threshold
        and consistent
        and trend != Trend.DECLINING
    ):
        return step_difficulty(anchor, +1)
    return anchor


def _pct(value: float) -> str:
    return f"{value:.0%}"


# --------------------------------------------------------------------------
# The decision
# --------------------------------------------------------------------------
def decide(data: AdaptiveInput, config: AdaptiveConfig = DEFAULT_CONFIG) -> RuleDecision:
    outcomes = list(data.recent_outcomes)
    performance = mr.recent_performance(outcomes)
    trend = compute_trend(outcomes, config)

    def result(action, difficulty, code, reason) -> RuleDecision:
        return RuleDecision(action, difficulty, code, reason, trend, performance)

    # 1. Follow-up: teaching was just delivered and nothing new has been answered.
    if (
        data.previous_action in (AdaptiveAction.TEACH, AdaptiveAction.REVISE)
        and data.attempts_at_previous_decision is not None
        and data.attempts == data.attempts_at_previous_decision
    ):
        return result(
            AdaptiveAction.PRACTICE,
            config.follow_up_difficulty,
            ReasonCode.FOLLOW_UP_PRACTICE,
            "The topic was just explained; check understanding with easy guided practice.",
        )

    # 2. No evidence on this topic yet.
    if data.attempts == 0:
        if data.lessons_completed == 0:
            return result(
                AdaptiveAction.TEACH,
                config.starting_difficulty,
                ReasonCode.NEW_TOPIC,
                "The student has not started this topic yet; introduce it first.",
            )
        return result(
            AdaptiveAction.PRACTICE,
            config.starting_difficulty,
            ReasonCode.FIRST_PRACTICE,
            "Lessons are done but no questions have been attempted; start with practice.",
        )

    # 3. Too little evidence to change course.
    if data.attempts < config.min_attempts_to_adapt:
        return result(
            AdaptiveAction.PRACTICE,
            data.previous_difficulty or config.starting_difficulty,
            ReasonCode.BUILDING_EVIDENCE,
            f"Only {data.attempts} attempt(s) so far; keep practising to gather reliable evidence "
            "before adapting.",
        )

    # 4. Enough evidence: apply the rules.
    mastery = data.mastery_score
    consistent = is_consistent(outcomes, config)
    strong = performance >= config.strong_performance_threshold

    # 4a. Significant difficulty: low mastery AND poor recent performance.
    if mastery < config.low_mastery_threshold and performance < config.poor_performance_threshold:
        return result(
            AdaptiveAction.REVISE,
            Difficulty.EASY,
            ReasonCode.LOW_MASTERY_POOR_PERFORMANCE,
            f"Mastery ({_pct(mastery)}) and recent performance ({_pct(performance)}) are both low; "
            "re-teach the topic before more questions.",
        )

    # 4b. Sufficiently mastered, consistently strong: move on.
    if (
        mastery >= config.progress_mastery_threshold
        and data.attempts >= config.min_attempts_to_progress
        and strong
        and consistent
    ):
        return result(
            AdaptiveAction.PROGRESS,
            None,
            ReasonCode.MASTERED_CONSISTENT,
            f"Mastery ({_pct(mastery)}) and recent performance ({_pct(performance)}) are consistently "
            "strong; ready for the next learning objective.",
        )

    # 4c. Strong but not yet proven: a more demanding check, not trivial repetition.
    if mastery >= config.proficient_mastery_threshold and strong:
        return result(
            AdaptiveAction.ASSESS,
            Difficulty.HARD if consistent else Difficulty.MEDIUM,
            ReasonCode.STRONG_NEEDS_CONFIRMATION,
            f"Mastery ({_pct(mastery)}) is proficient and recent performance ({_pct(performance)}) is "
            "strong; confirm understanding with a more demanding question.",
        )

    # 4d. Developing / mixed: practise, adjusting difficulty by one level at most.
    difficulty = select_practice_difficulty(
        mastery, performance, trend, consistent, data.previous_difficulty, config
    )
    if performance < config.difficulty_decrease_threshold:
        code = ReasonCode.PERFORMANCE_DROP
        reason = (
            f"Recent performance ({_pct(performance)}) is below target; practise at "
            f"{difficulty.value} difficulty."
        )
    else:
        code = ReasonCode.DEVELOPING_MIXED
        reason = (
            f"Mastery ({_pct(mastery)}) is still developing with mixed recent performance "
            f"({_pct(performance)}); practise at {difficulty.value} difficulty."
        )
    return result(AdaptiveAction.PRACTICE, difficulty, code, reason)