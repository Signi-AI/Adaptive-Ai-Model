"""api/routes/mastery.py  (Issue 06) -- read-only; student id comes from the token."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_student_id      # see note in routes/progress.py
from app.core.curriculum_ids import TopicId
from app.core.database import get_db
from app.schemas.mastery import StudentLearningState, TopicMasteryDetail
from app.services.mastery_service import MasteryService

router = APIRouter(prefix="/mastery", tags=["Mastery"])


@router.get("", response_model=StudentLearningState)
def get_my_mastery(
    student_id: UUID = Depends(get_current_student_id),
    db: Session = Depends(get_db),
):
    return MasteryService.get_student_learning_state(db, student_id)


@router.get("/topics/{topic_id}", response_model=TopicMasteryDetail)
def get_my_topic_mastery(
    topic_id: TopicId,
    student_id: UUID = Depends(get_current_student_id),
    db: Session = Depends(get_db),
):
    try:
        return MasteryService.get_topic_mastery_detail(db, student_id, topic_id)
    except LookupError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
