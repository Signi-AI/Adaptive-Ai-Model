from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.curriculum_service import CurriculumService

router = APIRouter(
    prefix="/students",
    tags=["Student Curriculum"],
)


@router.get("/me/curriculum")
def get_my_curriculum(
    db: Session = Depends(get_db),
):
    if curriculum := CurriculumService.get_curriculum_by_academic_level(
        db,
        academic_level_id=1,
    ):
        return curriculum

    raise HTTPException(
            status_code=404,
            detail="Curriculum not found",
        )