from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from backend.app.schemas.assessment import (
    SubmitAnswerRequest,
    AssessmentResponse,
    ErrorResponse,
)
from backend.app.services.assessment_service import (
    AssessmentService,
    AssessmentError,
    default_assessment_service,
)


Response = Tuple[int, Dict[str, Any]]


def submit_answer(
    body: Dict[str, Any],
    service: Optional[AssessmentService] = None,
) -> Response:
    """
    POST /assessments/submit

    Body:
        {
            "question_id": "...",
            "student_id": "...",
            "answer": <number | string>,
            "absolute_tolerance": 1e-6,   # optional
            "relative_tolerance": 1e-6    # optional
        }
    """
    svc = service or default_assessment_service
    try:
        request = SubmitAnswerRequest.from_dict(body)
    except (ValueError, TypeError, KeyError) as exc:
        err = ErrorResponse(detail=str(exc), code="validation_error")
        return 400, err.to_dict()

    try:
        result: AssessmentResponse = svc.submit_answer(request)
    except AssessmentError as exc:
        status = 404 if exc.code == "question_not_found" else 400
        err = ErrorResponse(detail=exc.message, code=exc.code)
        return status, err.to_dict()

    return 200, result.to_dict()


def get_attempt(
    attempt_id: str,
    service: Optional[AssessmentService] = None,
) -> Response:
    """GET /assessments/attempts/{attempt_id}"""
    svc = service or default_assessment_service
    attempt = svc.get_attempt(attempt_id)
    if attempt is None:
        err = ErrorResponse(detail=f"Attempt not found: {attempt_id}", code="not_found")
        return 404, err.to_dict()
    return 200, attempt.to_dict()


def list_student_attempts(
    student_id: str,
    service: Optional[AssessmentService] = None,
) -> Response:
    """GET /assessments/students/{student_id}/attempts"""
    svc = service or default_assessment_service
    result = svc.list_attempts_for_student(student_id)
    return 200, result.to_dict()


def list_question_attempts(
    question_id: str,
    service: Optional[AssessmentService] = None,
) -> Response:
    """GET /assessments/questions/{question_id}/attempts"""
    svc = service or default_assessment_service
    result = svc.list_attempts_for_question(question_id)
    return 200, result.to_dict()
