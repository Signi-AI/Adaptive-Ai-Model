
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence


@dataclass
class DifficultyProfile:
    """Constraints that characterise a difficulty band."""
    name: str                                  # e.g. "easy", "medium", "hard"
    min_value: Optional[float] = None          # absolute lower bound on any param
    max_value: Optional[float] = None          # absolute upper bound
    max_digits: Optional[int] = None           # max integer digits allowed
    forbidden_ops: Sequence[str] = ()          # ops that must not appear in answer path
    required_ops: Sequence[str] = ()           # ops that must appear


# Default profiles – can be overridden per template
DEFAULT_PROFILES: Dict[str, DifficultyProfile] = {
    "easy": DifficultyProfile(
        name="easy",
        min_value=1,
        max_value=20,
        max_digits=2,
    ),
    "medium": DifficultyProfile(
        name="medium",
        min_value=1,
        max_value=50,
        max_digits=2,
    ),
    "hard": DifficultyProfile(
        name="hard",
        min_value=1,
        max_value=50,
        max_digits=2,
    ),
}


class DifficultyValidator:
    """
    Validates a generated parameter dictionary against a difficulty profile.

    Returns True when the values are acceptable for the requested level.
    """

    def __init__(self, profiles: Optional[Dict[str, DifficultyProfile]] = None):
        self.profiles = profiles or dict(DEFAULT_PROFILES)

    def validate(
        self,
        values: Dict[str, Any],
        difficulty: str,
        extra_checks: Optional[List[str]] = None,
    ) -> bool:
        profile = self.profiles.get(difficulty)
        if profile is None:
            # Unknown difficulty – accept by default (or raise, depending on policy)
            return True

        for name, val in values.items():
            if not isinstance(val, (int, float)):
                continue
            if profile.min_value is not None and val < profile.min_value:
                return False
            if profile.max_value is not None and val > profile.max_value:
                return False
            if profile.max_digits is not None and isinstance(val, int):
                if len(str(abs(val))) > profile.max_digits:
                    return False

        # extra_checks are free-form boolean expressions evaluated against values
        if extra_checks:
            from backend.app.questions.parameter_engine import safe_eval
            for expr in extra_checks:
                try:
                    if not bool(safe_eval(expr, values)):
                        return False
                except Exception:
                    return False

        return True

    def filter_valid(
        self,
        candidates: List[Dict[str, Any]],
        difficulty: str,
    ) -> List[Dict[str, Any]]:
        """Return only those candidate value sets that pass validation."""
        return [c for c in candidates if self.validate(c, difficulty)]