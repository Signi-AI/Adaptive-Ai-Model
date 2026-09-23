from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.assessment import AnswerSubmissionRequest, AssessmentResultResponse
from app.services.assessment_service import AssessmentError, AssessmentService

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.post(
    "/submit",
    response_model=AssessmentResultResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a student's answer to a generated question",
)
def submit_answer(
    payload: AnswerSubmissionRequest,
    db: Session = Depends(get_db),
) -> AssessmentResultResponse:

    service = AssessmentService(db)
    try:
        attempt = service.submit_answer(
            generated_question_id=payload.generated_question_id,
            submitted_answer=payload.submitted_answer,
            session_id=payload.session_id,
        )
    except AssessmentError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return attempt