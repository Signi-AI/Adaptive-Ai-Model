"""mastery_rules.py

Pure, deterministic mastery maths for Issue 06. No database, no FastAPI,
no SQLAlchemy -- only the standard library -- so every rule here can be
unit-tested in isolation and tuned in one place.

Model in one paragraph
----------------------
Mastery is a 0..1 score per (student, topic) and, when the attempt names a
learning objective, per (student, learning objective). Each completed
attempt nudges the score toward that attempt's outcome:

    new = old + alpha * (outcome - old)

* The first few attempts use alpha = 1 / (n + 1), i.e. a running average that
  starts from a neutral 0.5 prior. After that alpha settles at ALPHA, so
  recent attempts always count more than old ones and a student can move up
  OR down.
* alpha is scaled by question difficulty, direction-aware: a hard question
  answered well moves the score more than an easy one; a hard question missed
  hurts less than an easy one missed.
* Status (BEGINNING..MASTERED) is read off the score, but gated by the number
  of attempts so one lucky answer can never look like mastery.
* Strength / weakness are derived on read, never stored by hand.
"""

from __future__ import annotations

from collections.abc import Sequence

# --------------------------------------------------------------------------
# Tunable constants (the only place thresholds live)
# --------------------------------------------------------------------------
INITIAL_SCORE = 0.5        # neutral prior used for the very first update
ALPHA = 0.2                # steady-state learning rate (~ last 5 attempts)

DIFFICULTY_MIN = 1
DIFFICULTY_MAX = 5
DIFFICULTY_DEFAULT = 3
DIFFICULTY_STEP = 0.2      # weight change per difficulty level away from 3

DEVELOPING_MIN = 0.40
PROFICIENT_MIN = 0.70
MASTERED_MIN = 0.85

MIN_ATTEMPTS_FOR_STATUS = 3     # below this a topic is always BEGINNING
MIN_ATTEMPTS_FOR_MASTERED = 5   # MASTERED needs at least this much evidence

MIN_ATTEMPTS_FOR_CLASSIFICATION = 5   # strength/weakness need this much evidence
STRENGTH_MIN_SCORE = 0.70
WEAKNESS_MAX_SCORE = 0.50

RECENT_WINDOW = 5


# Status names are plain strings here; models/mastery.py exposes the same
# values as the MasteryStatus enum (str-valued, so they compare equal).
BEGINNING = "BEGINNING"
DEVELOPING = "DEVELOPING"
PROFICIENT = "PROFICIENT"
MASTERED = "MASTERED"


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def clamp_difficulty(difficulty: int | None) -> int:
    if difficulty is None:
        return DIFFICULTY_DEFAULT
    return max(DIFFICULTY_MIN, min(DIFFICULTY_MAX, int(difficulty)))


def difficulty_weight(difficulty: int | None, improving: bool) -> float:
    """
    Multiplier applied to alpha.

    improving=True  (outcome is above the current score): harder -> bigger move.
    improving=False (outcome is below the current score): harder -> smaller move.
    Range with defaults: 0.6 .. 1.4, and exactly 1.0 at the default level 3.
    """
    offset = (clamp_difficulty(difficulty) - DIFFICULTY_DEFAULT) * DIFFICULTY_STEP
    return 1.0 + offset if improving else 1.0 - offset


def learning_rate(attempts_before: int) -> float:
    """Running-average rate for early attempts, ALPHA once evidence builds up."""
    n = max(0, attempts_before) + 1          # ordinal of the attempt being applied
    return max(1.0 / (n + 1), ALPHA)


def apply_attempt(
    old_score: float,
    attempts_before: int,
    outcome: float,
    difficulty: int | None = DIFFICULTY_DEFAULT,
) -> float:
    """
    Return the new mastery score after one attempt.

    old_score       current score (use INITIAL_SCORE when attempts_before == 0)
    attempts_before attempts already counted for this row
    outcome         this attempt's score in 0..1 (1 = fully correct)
    difficulty      1 (easy) .. 5 (hard); None -> default
    """
    if not 0.0 <= outcome <= 1.0:
        raise ValueError("outcome must be between 0 and 1")
    old = clamp(old_score)
    improving = outcome >= old
    alpha = min(1.0, learning_rate(attempts_before) * difficulty_weight(difficulty, improving))
    return clamp(old + alpha * (outcome - old))


def classify_status(score: float, attempts: int) -> str:
    """Map (score, evidence) to a status. Reversible: recomputed on every update."""
    if attempts < MIN_ATTEMPTS_FOR_STATUS or score < DEVELOPING_MIN:
        return BEGINNING
    if score < PROFICIENT_MIN:
        return DEVELOPING
    if score < MASTERED_MIN or attempts < MIN_ATTEMPTS_FOR_MASTERED:
        return PROFICIENT
    return MASTERED


def is_strength(score: float, attempts: int) -> bool:
    return attempts >= MIN_ATTEMPTS_FOR_CLASSIFICATION and score >= STRENGTH_MIN_SCORE


def is_weakness(score: float, attempts: int) -> bool:
    return attempts >= MIN_ATTEMPTS_FOR_CLASSIFICATION and score < WEAKNESS_MAX_SCORE


def recent_performance(recent_outcomes: Sequence[float]) -> float:
    """
    Mean outcome of the most recent attempts (callers pass at most
    RECENT_WINDOW values, newest first). 0.0 when there is no evidence yet.
    """
    window = list(recent_outcomes)[:RECENT_WINDOW]
    if not window:
        return 0.0
    return sum(window) / len(window)


def percentage(part: int | float, whole: int | float) -> float:
    """part / whole as a 0..1 fraction; 0.0 when whole is 0 (never divides by zero)."""
    return 0.0 if not whole else part / whole