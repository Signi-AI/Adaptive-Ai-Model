from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.curriculum_service import CurriculumService
from app.schemas.learning_objective import (
    LearningObjectiveCreate,
    LearningObjectiveUpdate,
    LearningObjectiveResponse,
)

router = APIRouter(
    prefix="/learning-objectives",
    tags=["Curriculum - Learning Objectives"],
)


# =========================
# Create Learning Objective
# =========================

@router.post(
    "/lesson/{lesson_id}",
    response_model=LearningObjectiveResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_learning_objective(
    lesson_id: int,
    objective_data: LearningObjectiveCreate,
    db: Session = Depends(get_db),
):
    try:
        return CurriculumService.create_learning_objective(
            db,
            lesson_id,
            objective_data,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


# =========================
# Get Objectives by Lesson
# =========================

@router.get(
    "/lesson/{lesson_id}",
    response_model=list[LearningObjectiveResponse],
)
def get_objectives_by_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
):
    objectives = CurriculumService.get_objectives_by_lesson(
        db,
        lesson_id,
    )

    if objectives is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found",
        )

    return objectives


# =========================
# Get Single Objective
# =========================

@router.get(
    "/{objective_id}",
    response_model=LearningObjectiveResponse,
)
def get_learning_objective(
    objective_id: int,
    db: Session = Depends(get_db),
):
    if objective := CurriculumService.get_learning_objective(
        db,
        objective_id,
    ):
        return objective

    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning objective not found",
    )
    
@router.put(
    "/{objective_id}",
    response_model=LearningObjectiveResponse,
)
def update_learning_objective(
    objective_id: int,
    objective_data: LearningObjectiveUpdate,
    db: Session = Depends(get_db),
):
    if objective := CurriculumService.update_learning_objective(
        db,
        objective_id,
        objective_data,
    ):
        return objective
        

    
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning objective not found",
        )


@router.patch(
    "/{objective_id}/deactivate",
    response_model=LearningObjectiveResponse,
)
def deactivate_learning_objective(
    objective_id: int,
    db: Session = Depends(get_db),
):
    if objective := CurriculumService.deactivate_learning_objective(
        db,
        objective_id,
    ):
        return objective
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Learning objective not found",
        )
