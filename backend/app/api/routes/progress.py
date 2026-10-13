"""api/routes/progress.py  (Issue 06)

The student id ALWAYS comes from the authenticated token, never from the URL
or query string -- there is no way to ask for someone else's progress.

ASSUMPTION: app/api/deps.py exposes `get_current_student_id`, a dependency that
returns the authenticated STUDENT's user id (UUID) and rejects other roles.
If yours is named differently, change this one import (and the same import in
routes/mastery.py, routes/adaptive.py and tests/conftest.py).
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_student_id
from app.core.curriculum_ids import AcademicLevelId, SubjectId, TopicId
from app.core.database import get_db
from app.schemas.progress import OverallProgress, SubjectProgress, TopicProgress
from app.services.progress_service import ProgressService

router = APIRouter(prefix="/progress", tags=["Progress"])


def _not_found(error: LookupError) -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))


@router.get("", response_model=OverallProgress)
def get_my_progress(
    academic_level_id: AcademicLevelId | None = None,
    student_id: UUID = Depends(get_current_student_id),
    db: Session = Depends(get_db),
):
    """Pass ?academic_level_id= to total only that level's curriculum."""
    return ProgressService.get_overall_progress(db, student_id, academic_level_id=academic_level_id)


@router.get("/subjects/{subject_id}", response_model=SubjectProgress)
def get_my_subject_progress(
    subject_id: SubjectId,
    academic_level_id: AcademicLevelId | None = None,
    student_id: UUID = Depends(get_current_student_id),
    db: Session = Depends(get_db),
):
    try:
        return ProgressService.get_subject_progress(
            db, student_id, subject_id, academic_level_id=academic_level_id
        )
    except LookupError as error:
        raise _not_found(error) from error


@router.get("/topics/{topic_id}", response_model=TopicProgress)
def get_my_topic_progress(
    topic_id: TopicId,
    student_id: UUID = Depends(get_current_student_id),
    db: Session = Depends(get_db),
):
    try:
        return ProgressService.get_topic_progress(db, student_id, topic_id)
    except LookupError as error:
        raise _not_found(error) from error
