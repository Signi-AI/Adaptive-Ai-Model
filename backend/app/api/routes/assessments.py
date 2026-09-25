from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.assessment import AnswerSubmissionRequest, AssessmentResultResponse
from app.services.assessment_service import AssessmentError, AssessmentService

editor_required = RoleChecker(["editor","super_admin"])
services = AssessmentService()

router = APIRouter(prefix="/assessments", tags=["assessments"])


@router.post(
    "/submit",
    response_model=AssessmentResultResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit a student's answer to a generated question",
)
def create_assesment(data:AssessmentServices , current_assesment: Users = Depends(editor_required), db: Session = Depends(get_db)):
    return services._assmentment_post_create(data, current_assesment, db)
