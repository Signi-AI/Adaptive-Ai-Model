from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.curriculum_service import CurriculumService
from app.schemas.academic_level import (
    AcademicLevelCreate,
    AcademicLevelUpdate,
    AcademicLevelResponse,
)

router = APIRouter(
    prefix="/academic-levels",
    tags=["Curriculum - Academic Levels"],
)


@router.post(
    "/",
    response_model=AcademicLevelResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_academic_level(
    academic_level_data: AcademicLevelCreate,
    db: Session = Depends(get_db),
):
    try:
        return CurriculumService.create_academic_level(
            db,
            academic_level_data,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error


@router.get(
    "/",
    response_model=list[AcademicLevelResponse],
)
def get_academic_levels(
    db: Session = Depends(get_db),
):
    return CurriculumService.get_academic_levels(db)


@router.get(
    "/{academic_level_id}",
    response_model=AcademicLevelResponse,
)
def get_academic_level(
    academic_level_id: int,
    db: Session = Depends(get_db),
):
    if academic_level := CurriculumService.get_academic_level(
        db,
        academic_level_id,
    ):
        return academic_level

    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Academic level not found",
        )



@router.put(
    "/{academic_level_id}",
    response_model=AcademicLevelResponse,
)
def update_academic_level(
    academic_level_id: int,
    academic_level_data: AcademicLevelUpdate,
    db: Session = Depends(get_db),
):
    if academic_level := CurriculumService.update_academic_level(
        db,
        academic_level_id,
        academic_level_data,
    ):
        return academic_level

    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Academic level not found",
        )
