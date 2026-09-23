from __future__ import annotations

from typing import Optional

from backend.app.questions.answer_engine import AnswerEngine, EvaluationResult
from backend.app.questions.generator import QuestionStore, default_store
from backend.app.models.attempt import Attempt, AttemptStore, default_attempt_store
from backend.app.schemas.assessment import (
    SubmitAnswerRequest,
    AssessmentResponse,
    AttemptListResponse,
)


class AssessmentError(Exception):
    def __init__(self, message: str, code: str = "assessment_error"):
        super().__init__(message)
        self.message = message
        self.code = code


class AssessmentService:
    def __init__(
        self,
        question_store: Optional[QuestionStore] = None,
        attempt_store: Optional[AttemptStore] = None,
        answer_engine: Optional[AnswerEngine] = None,
    ):
        self.question_store = question_store or default_store
        self.attempt_store = attempt_store or default_attempt_store
        self.answer_engine = answer_engine or AnswerEngine()

    def submit_answer(self, request: SubmitAnswerRequest) -> AssessmentResponse:
        question = self.question_store.get(request.question_id)
        if question is None:
            raise AssessmentError(
                f"Question not found: {request.question_id}",
                code="question_not_found",
            )

        result: EvaluationResult = self.answer_engine.evaluate(
            question,
            request.answer,
            absolute_tolerance=request.absolute_tolerance,
            relative_tolerance=request.relative_tolerance,
        )

        attempt = Attempt.create(
            question_id=request.question_id,
            student_id=request.student_id,
            submitted_answer=result.submitted,
            expected_answer=result.expected,
            is_correct=result.is_correct,
            feedback=result.feedback,
            tolerance_used=result.tolerance_used,
            metadata={"error": result.error} if result.error else {},
        )
        self.attempt_store.save(attempt)

        return AssessmentResponse(
            attempt_id=attempt.id,
            question_id=attempt.question_id,
            student_id=attempt.student_id,
            is_correct=attempt.is_correct,
            expected_answer=attempt.expected_answer,
            submitted_answer=attempt.submitted_answer,
            feedback=attempt.feedback,
            tolerance_used=attempt.tolerance_used,
            error=result.error,
            created_at=attempt.created_at,
        )

    def get_attempt(self, attempt_id: str) -> Optional[Attempt]:
        return self.attempt_store.get(attempt_id)

    def list_attempts_for_student(self, student_id: str) -> AttemptListResponse:
        items = self.attempt_store.list_by_student(student_id)
        return AttemptListResponse(
            attempts=[a.to_dict() for a in items],
            count=len(items),
        )

    def list_attempts_for_question(self, question_id: str) -> AttemptListResponse:
        items = self.attempt_store.list_by_question(question_id)
        return AttemptListResponse(
            attempts=[a.to_dict() for a in items],
            count=len(items),
        )


default_assessment_service = AssessmentService()