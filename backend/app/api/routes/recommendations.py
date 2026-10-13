"""api/routes/recommendations.py  (Issue 08)

The student id ALWAYS comes from the authenticated token. A recommendation that
belongs to someone else is reported as 404, exactly like one that does not exist.

Generation is intentionally NOT an endpoint: recommendations are produced by the
backend learning flow (RecommendationService.generate_from_decision) from a
persisted adaptive decision, never requested by the client.

  GET   /recommendations                  current (open) recommendations, most urgent first
                                          ?history=true  all statuses, newest first
                                          ?status=COMPLETED&status=DISMISSED  explicit filter
                                          ?topic_id= / ?subject_id=  narrow down
  GET   /recommendations/{id}             one recommendation
  PATCH /recommendations/{id}/status      ACTIVE | COMPLETED | DISMISSED
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status as http_status
from sqlalchemy.orm import Session

from app.api.deps import get_current_student_id      # see note in routes/progress.py
from app.core.curriculum_ids import SubjectId, TopicId
from app.core.database import get_db
from app.core.learning_enums import RecommendationStatus
from app.schemas.recommendation import RecommendationOut, RecommendationStatusUpdate
from app.services.recommendation_service import InvalidStatusTransition, RecommendationService

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("", response_model=list[RecommendationOut])
def list_my_recommendations(
    status_filter: list[RecommendationStatus] | None = Query(default=None, alias="status"),
    topic_id: TopicId | None = None,
    subject_id: SubjectId | None = None,
    history: bool = False,
    limit: int = Query(default=100, ge=1, le=200),
    student_id: UUID = Depends(get_current_student_id),
    db: Session = Depends(get_db),
):
    return RecommendationService.list_recommendations(
        db,
        student_id,
        statuses=status_filter,
        topic_id=topic_id,
        subject_id=subject_id,
        include_history=history,
        limit=limit,
    )


@router.get("/{recommendation_id}", response_model=RecommendationOut)
def get_my_recommendation(
    recommendation_id: int,
    student_id: UUID = Depends(get_current_student_id),
    db: Session = Depends(get_db),
):
    try:
        return RecommendationService.get_recommendation(db, student_id, recommendation_id)
    except LookupError as error:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@router.patch("/{recommendation_id}/status", response_model=RecommendationOut)
def update_my_recommendation_status(
    recommendation_id: int,
    body: RecommendationStatusUpdate,
    student_id: UUID = Depends(get_current_student_id),
    db: Session = Depends(get_db),
):
    try:
        return RecommendationService.update_status(db, student_id, recommendation_id, body.status)
    except LookupError as error:
        raise HTTPException(status_code=http_status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except InvalidStatusTransition as error:
        raise HTTPException(status_code=http_status.HTTP_409_CONFLICT, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
