
import math
import re
from dataclasses import dataclass
from typing import Any, Union


class AnswerValidationError(Exception):
    """Inatolewa pale jibu lililotumwa na mwanafunzi si sahihi kimuundo (invalid submission)."""
@dataclass(frozen=True)

class AnswerEvaluationResult:

    is_correct: bool
    expected_answer: Union[int, float]
    submitted_answer: Union[int, float]


class AnswerEngine(object):

    NUMERIC_ABS_TOLERANCE = 1e-6
    NUMERIC_REL_TOLERANCE = 1e-6

    # Muundo wa maandishi unaokubalika kuwa "namba kamili" (integer),
    # ukiruhusu alama ya + au - mbele
    _INTEGER_PATTERN = re.compile(r"^[+-]?\d+$")

    def evaluate(self, correct_answer: Any, submitted_answer: Any) -> AnswerEvaluationResult:
    
        expected = self._normalize_numeric(correct_answer, source="stored correct_answer")
        submitted = self._normalize_numeric(submitted_answer, source="submitted answer")

        is_correct = self._numbers_match(expected, submitted)

        return AnswerEvaluationResult(
            is_correct=is_correct,
            expected_answer=expected,
            submitted_answer=submitted,
        )

    

    def _normalize_numeric(self, value: Any, source: str) -> Union[int, float]:
    
        # bool ni subclass ya int kwenye Python (True == 1) — tunaikataa
        # wazi hapa ili isije "ikapita" kimakosa kama namba halali.
        if isinstance(value, bool):
            raise AnswerValidationError(
                f"{source} is a boolean, not a numeric value: {value!r}"
            )

        if isinstance(value, (int, float)):
            if isinstance(value, float) and not math.isfinite(value):
                raise AnswerValidationError(
                    f"{source} is not a finite number (NaN/infinity): {value}"
                )
            return value

        if isinstance(value, str):
            return self._normalize_string_value(value, source)

        raise AnswerValidationError(
            f"{source} has an unsupported type for numeric comparison: {type(value).__name__}"
        )

    def _normalize_string_value(self, value: str, source: str) -> Union[int, float]:

        stripped = value.strip()
        if not stripped:
            raise AnswerValidationError(f"{source} is empty.")

        if self._INTEGER_PATTERN.match(stripped):
            return int(stripped)

        try:
            parsed = float(stripped)
        except ValueError as exc:
            raise AnswerValidationError(
                f"{source} '{value}' is not a valid number."
            ) from exc

        if not math.isfinite(parsed):
            raise AnswerValidationError(
                f"{source} '{value}' is not a finite number (NaN/infinity)."
            )
        return parsed

    def _numbers_match(self, expected: Union[int, float], submitted: Union[int, float]) -> bool:

        if isinstance(expected, int) and isinstance(submitted, int):
            return expected == submitted

        return math.isclose(
            float(expected),
            float(submitted),
            rel_tol=self.NUMERIC_REL_TOLERANCE,
            abs_tol=self.NUMERIC_ABS_TOLERANCE,
        )