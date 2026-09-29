from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.curriculum_service import CurriculumService
from app.schemas.topic import (
    TopicCreate,
    TopicUpdate,
    TopicResponse,
)

router = APIRouter(
    prefix="/topics",
    tags=["Curriculum - Topics"],
)


# =========================
# Create Topic
# =========================

@router.post(
    "/subject/{subject_id}",
    response_model=TopicResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_topic(
    subject_id: int,
    topic_data: TopicCreate,
    db: Session = Depends(get_db),
):
    try:
        return CurriculumService.create_topic(
            db,
            subject_id,
            topic_data,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


# =========================
# Get Topic
# =========================

@router.get(
    "/{topic_id}",
    response_model=TopicResponse,
)
def get_topic(
    topic_id: int,
    db: Session = Depends(get_db),
):
    if topic := CurriculumService.get_topic(
        db,
        topic_id,
    ):
        return topic

    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found",
        )




# =========================
# Get Topics by Subject
# =========================

@router.get(
    "/subject/{subject_id}",
    response_model=list[TopicResponse],
)
def get_topics_by_subject(
    subject_id: int,
    db: Session = Depends(get_db),
):
    topics = CurriculumService.get_topics_by_subject(
        db,
        subject_id,
    )

    if topics is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )

    return topics


# =========================
# Update Topic
# =========================

@router.put(
    "/{topic_id}",
    response_model=TopicResponse,
)
def update_topic(
    topic_id: int,
    topic_data: TopicUpdate,
    db: Session = Depends(get_db),
):
    if topic := CurriculumService.update_topic(
        db,
        topic_id,
        topic_data,
    ):
        return topic

    
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found",
        )


# =========================
# Deactivate Topic
# =========================

@router.patch(
    "/{topic_id}/deactivate",
    response_model=TopicResponse,
)
def deactivate_topic(
    topic_id: int,
    db: Session = Depends(get_db),
):
    if topic := CurriculumService.deactivate_topic(
        db,
        topic_id,
    ):
        return topic

    
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found",
        )
