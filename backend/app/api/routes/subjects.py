from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID 

from app.core.database import get_db
from app.services.curriculum_service import CurriculumService
from app.schemas.subject import (
    SubjectCreate,
    SubjectUpdate,
    SubjectResponse,
)

router = APIRouter(
    prefix="/subjects",
    tags=["Curriculum - Subjects"],
)

@router.post(
    "/",
    response_model=SubjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_subject(
    subject_data: SubjectCreate,
    db: Session = Depends(get_db),
):
    try:
        return CurriculumService.create_subject(
            db,
            subject_data,
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

@router.get(
    "/",
    response_model=list[SubjectResponse],
)
def get_subjects(
    academic_level_id: UUID | None = None,  # Updated filtering id type if applicable
    db: Session = Depends(get_db),
):
    return CurriculumService.get_subjects(
        db,
        academic_level_id,
    )

@router.get(
    "/{subject_id}",
    response_model=SubjectResponse,
)
def get_subject(
    subject_id: UUID,  # Changed from int to UUID
    db: Session = Depends(get_db),
):
    if subject := CurriculumService.get_subject(
        db,
        subject_id,
    ):
        return subject

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Subject not found",
    )

@router.put(
    "/{subject_id}",
    response_model=SubjectResponse,
)
def update_subject(
    subject_id: UUID,  # Changed from int to UUID
    subject_data: SubjectUpdate,
    db: Session = Depends(get_db),
):
    if subject := CurriculumService.update_subject(
        db,
        subject_id,
        subject_data,
    ):
        return subject

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Subject not found",
    )

@router.patch(
    "/{subject_id}/deactivate",
    response_model=SubjectResponse,
)
def deactivate_subject(
    subject_id: UUID,  
    db: Session = Depends(get_db),
):
    if subject := CurriculumService.deactivate_subject(
        db,
        subject_id,
    ):
        return subject

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Subject not found",
    )
