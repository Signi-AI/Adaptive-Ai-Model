

#from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any, Optional, Union

from backend.app.questions.generator import GeneratedQuestion


@dataclass
class EvaluationResult:
    """Outcome of comparing a student answer to the expected answer."""
    is_correct: bool
    expected: Any
    submitted: Any
    feedback: str
    tolerance_used: Optional[float] = None
    error: Optional[str] = None

    @property
    def is_valid_submission(self) -> bool:
        return self.error is None


_NUMBER_RE = re.compile(
    r"""
    ^\s*
    [+-]?
    (?:
        \d+\.?\d*
        |
        \.\d+
    )
    (?:[eE][+-]?\d+)?
    \s*$
    """,
    re.VERBOSE,
)


def parse_numerical(raw: Any) -> float:
    """Convert a student submission into a float. Raises ValueError on failure."""
    if isinstance(raw, bool):
        raise ValueError("Boolean is not a valid numerical answer")
    if isinstance(raw, (int, float)):
        if math.isnan(raw) or math.isinf(raw):
            raise ValueError("NaN / Inf are not valid answers")
        return float(raw)
    if isinstance(raw, str):
        text = raw.strip().replace(",", "")
        if not text:
            raise ValueError("Empty answer")
        if not _NUMBER_RE.match(text):
            raise ValueError(f"Cannot parse as number: {raw!r}")
        val = float(text)
        if math.isnan(val) or math.isinf(val):
            raise ValueError("NaN / Inf are not valid answers")
        return val
    raise ValueError(f"Unsupported answer type: {type(raw).__name__}")


def parse_exact(raw: Any) -> str:
    """Normalise an exact (non-numeric) answer to a comparable string."""
    if raw is None:
        raise ValueError("Empty answer")
    return str(raw).strip().lower()


def numbers_equal(
    expected: float,
    submitted: float,
    *,
    absolute_tolerance: float = 1e-6,
    relative_tolerance: float = 1e-6,
) -> bool:
    return math.isclose(
        expected,
        submitted,
        rel_tol=relative_tolerance,
        abs_tol=absolute_tolerance,
    )


def exact_equal(expected: str, submitted: str) -> bool:
    return expected == submitted


class AnswerEngine:
    """Evaluates a student answer against a GeneratedQuestion."""

    def __init__(
        self,
        absolute_tolerance: float = 1e-6,
        relative_tolerance: float = 1e-6,
    ):
        self.absolute_tolerance = absolute_tolerance
        self.relative_tolerance = relative_tolerance

    def expected_answer(self, question: GeneratedQuestion) -> Any:
        if question.answer is not None:
            return question.answer
        raise ValueError("GeneratedQuestion has no answer field")

    def evaluate(
        self,
        question: GeneratedQuestion,
        student_answer: Any,
        *,
        absolute_tolerance: Optional[float] = None,
        relative_tolerance: Optional[float] = None,
    ) -> EvaluationResult:
        expected = self.expected_answer(question)
        abs_tol = (
            absolute_tolerance
            if absolute_tolerance is not None
            else self.absolute_tolerance
        )
        rel_tol = (
            relative_tolerance
            if relative_tolerance is not None
            else self.relative_tolerance
        )

        if isinstance(expected, (int, float)) and not isinstance(expected, bool):
            return self._evaluate_numerical(
                expected, student_answer, abs_tol, rel_tol
            )
        return self._evaluate_exact(expected, student_answer)

    def _evaluate_numerical(
        self,
        expected: Union[int, float],
        student_answer: Any,
        abs_tol: float,
        rel_tol: float,
    ) -> EvaluationResult:
        try:
            submitted = parse_numerical(student_answer)
        except ValueError as exc:
            return EvaluationResult(
                is_correct=False,
                expected=expected,
                submitted=student_answer,
                feedback="Invalid numerical answer",
                error=str(exc),
            )

        expected_f = float(expected)
        correct = numbers_equal(
            expected_f,
            submitted,
            absolute_tolerance=abs_tol,
            relative_tolerance=rel_tol,
        )
        feedback = "Correct" if correct else "Incorrect"
        return EvaluationResult(
            is_correct=correct,
            expected=expected,
            submitted=submitted,
            feedback=feedback,
            tolerance_used=abs_tol,
        )

    def _evaluate_exact(
        self,
        expected: Any,
        student_answer: Any,
    ) -> EvaluationResult:
        try:
            submitted = parse_exact(student_answer)
            expected_norm = parse_exact(expected)
        except ValueError as exc:
            return EvaluationResult(
                is_correct=False,
                expected=expected,
                submitted=student_answer,
                feedback="Invalid answer",
                error=str(exc),
            )

        correct = exact_equal(expected_norm, submitted)
        feedback = "Correct" if correct else "Incorrect"
        return EvaluationResult(
            is_correct=correct,
            expected=expected,
            submitted=submitted,
            feedback=feedback,
        )


default_engine = AnswerEngine()


def evaluate_answer(
    question: GeneratedQuestion,
    student_answer: Any,
    **kwargs,
) -> EvaluationResult:
    return default_engine.evaluate(question, student_answer, **kwargs)