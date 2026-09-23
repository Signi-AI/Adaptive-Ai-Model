
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class SubmitAnswerRequest:
    """Body of POST /assessments/submit."""
    question_id: str
    student_id: str
    answer: Any
    absolute_tolerance: Optional[float] = None
    relative_tolerance: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SubmitAnswerRequest":
        required = ("question_id", "student_id", "answer")
        missing = [k for k in required if k not in data]
        if missing:
            raise ValueError(f"Missing required fields: {missing}")
        return cls(
            question_id=str(data["question_id"]),
            student_id=str(data["student_id"]),
            answer=data["answer"],
            absolute_tolerance=data.get("absolute_tolerance"),
            relative_tolerance=data.get("relative_tolerance"),
        )


@dataclass
class AssessmentResponse:
    """Returned after evaluating a student answer."""
    attempt_id: str
    question_id: str
    student_id: str
    is_correct: bool
    expected_answer: Any
    submitted_answer: Any
    feedback: str
    tolerance_used: Optional[float] = None
    error: Optional[str] = None
    created_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AttemptListResponse:
    attempts: List[Dict[str, Any]] = field(default_factory=list)
    count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ErrorResponse:
    detail: str
    code: str = "validation_error"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)