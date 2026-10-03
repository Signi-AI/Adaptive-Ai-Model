"""core/learning_enums.py

Shared vocabulary for the mastery (Issue 06) and adaptive (Issue 07) domains.
Standard library only, so the pure rule modules, the ORM models and the
Pydantic schemas can all import it without pulling each other in.

All enums are str-valued: they serialise to plain JSON strings and compare
equal to their string values.
"""

from enum import Enum


class MasteryStatus(str, Enum):
    """Learning-state classification. Reversible -- never a permanent label."""

    BEGINNING = "BEGINNING"
    DEVELOPING = "DEVELOPING"
    PROFICIENT = "PROFICIENT"
    MASTERED = "MASTERED"


class AdaptiveAction(str, Enum):
    """What should happen next. Deliberately small (see Issue 07, section 6)."""

    TEACH = "TEACH"        # introduce the topic / lesson
    REVISE = "REVISE"      # re-explain: the student is struggling
    PRACTICE = "PRACTICE"  # ask practice questions at the chosen difficulty
    ASSESS = "ASSESS"      # check understanding with a more demanding question
    PROGRESS = "PROGRESS"  # topic is sufficiently mastered: move on


class Difficulty(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"


class Trend(str, Enum):
    IMPROVING = "IMPROVING"
    STABLE = "STABLE"
    DECLINING = "DECLINING"
    UNKNOWN = "UNKNOWN"    # not enough history to say


class ReasonCode(str, Enum):
    """Machine-readable 'why', for the Recommendation / Teacher services."""

    NEW_TOPIC = "NEW_TOPIC"
    FIRST_PRACTICE = "FIRST_PRACTICE"
    FOLLOW_UP_PRACTICE = "FOLLOW_UP_PRACTICE"
    BUILDING_EVIDENCE = "BUILDING_EVIDENCE"
    LOW_MASTERY_POOR_PERFORMANCE = "LOW_MASTERY_POOR_PERFORMANCE"
    PERFORMANCE_DROP = "PERFORMANCE_DROP"
    DEVELOPING_MIXED = "DEVELOPING_MIXED"
    STRONG_NEEDS_CONFIRMATION = "STRONG_NEEDS_CONFIRMATION"
    MASTERED_CONSISTENT = "MASTERED_CONSISTENT"