from fastapi import APIRouter
from app.schemas.progress import ProgressResponse
from app.services.progress_service import ProgressService

router = APIRouter(prefix="/progress", tags=["progress"])
service = ProgressService()


@router.get("/{student_id}", response_model=ProgressResponse)
def get_progress(student_id: int):
    # Route only calls the service — no business logic here
    return service.get_student_progress(student_id)