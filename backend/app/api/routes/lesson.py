from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.curriculum_service import CurriculumService
from app.schemas.lesson import (
    LessonCreate,
    LessonUpdate,
    LessonResponse,
)

router = APIRouter(
    prefix="/lessons",
    tags=["Curriculum - Lessons"],
)


# =========================
# Create Lesson
# =========================

@router.post(
    "/topic/{topic_id}",
    response_model=LessonResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_lesson(
    topic_id: int,
    lesson_data: LessonCreate,
    db: Session = Depends(get_db),
):
    try:
        return CurriculumService.create_lesson(
            db,
            topic_id,
            lesson_data,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


# =========================
# Get Lessons by Topic
# =========================

@router.get(
    "/topic/{topic_id}",
    response_model=list[LessonResponse],
)
def get_lessons_by_topic(
    topic_id: int,
    db: Session = Depends(get_db),
):
    lessons = CurriculumService.get_lessons_by_topic(
        db,
        topic_id,
    )

    if lessons is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Topic not found",
        )

    return lessons


# =========================
# Get Single Lesson
# =========================

@router.get(
    "/{lesson_id}",
    response_model=LessonResponse,
)
def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
):
    if lesson := CurriculumService.get_lesson(
        db,
        lesson_id,
    ):
        return lesson
    
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )




# =========================
# Update Lesson
# =========================

@router.put(
    "/{lesson_id}",
    response_model=LessonResponse,
)
def update_lesson(
    lesson_id: int,
    lesson_data: LessonUpdate,
    db: Session = Depends(get_db),
):
    if lesson := CurriculumService.update_lesson(
        db,
        lesson_id,
        lesson_data,
    ):
        return lesson

    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )



# =========================
# Deactivate Lesson
# =========================

@router.patch(
    "/{lesson_id}/deactivate",
    response_model=LessonResponse,
)
def deactivate_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
):
    if lesson := CurriculumService.deactivate_lesson(
        db,
        lesson_id,
    ):
        return lesson
    
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )
