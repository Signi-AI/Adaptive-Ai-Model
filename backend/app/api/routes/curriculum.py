from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.curriculum_service import CurriculumService
from app.schemas.curriculum import CurriculumResponse


router = APIRouter(
    prefix="/curriculum",
    tags=["Curriculum"],
)


@router.get(
    "/academic-level/{academic_level_id}",
    response_model=CurriculumResponse,
)
def get_curriculum(
    academic_level_id: int,
    db: Session = Depends(get_db),
):
    if curriculum := CurriculumService.get_curriculum_by_academic_level(
        db,
        academic_level_id,
    ):
        return curriculum

    
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Academic level not found",
        )

