from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

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
    subject_id: UUID,
    topic_data: TopicCreate,
    db: Session = Depends(get_db),
):
    try:
        return CurriculumService.create_topic(
            db,
            subject_id,
            topic_data.name,
            topic_data.description,
            topic_data.sequence,
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
    topic_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        return CurriculumService.get_topic(db, topic_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error




# =========================
# Get Topics by Subject
# =========================

@router.get(
    "/subject/{subject_id}",
    response_model=list[TopicResponse],
)
def get_topics_by_subject(
    subject_id: UUID,
    db: Session = Depends(get_db),
):
    try:
        return CurriculumService.get_topics_by_subject(db, subject_id)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


# =========================
# Update Topic
# =========================

@router.put(
    "/{topic_id}",
    response_model=TopicResponse,
)
def update_topic(
    topic_id: UUID,
    topic_data: TopicUpdate,
    db: Session = Depends(get_db),
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Topic updates are not available")


# =========================
# Deactivate Topic
# =========================

@router.patch(
    "/{topic_id}/deactivate",
    response_model=TopicResponse,
)
def deactivate_topic(
    topic_id: UUID,
    db: Session = Depends(get_db),
):
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Topic updates are not available")
