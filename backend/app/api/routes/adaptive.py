"""api/routes/adaptive.py  (Issue 07) -- deliberately minimal.

The primary consumer is the backend learning flow, which calls
AdaptiveService.decide_next_action(...) directly. These two endpoints exist
for the frontend/debugging:

  GET  /adaptive/{topic_id}  preview of the decision right now. Persists nothing.
  POST /adaptive/decide      take AND record the decision for the learning step.

The student id comes from the token only (see note in routes/progress.py).
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_student_id
from app.core.database import get_db
from app.schemas.adaptive import AdaptiveDecideRequest, AdaptiveDecisionOut
from app.services.adaptive_service import AdaptiveService

router = APIRouter(prefix="/adaptive", tags=["Adaptive Learning"])


@router.get("/{topic_id}", response_model=AdaptiveDecisionOut)
def preview_decision(
    topic_id: int,
    student_id: UUID = Depends(get_current_student_id),
    db: Session = Depends(get_db),
):
    try:
        return AdaptiveService.decide_next_action(db, student_id, topic_id, persist=False)
    except LookupError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@router.post("/decide", response_model=AdaptiveDecisionOut)
def record_decision(
    body: AdaptiveDecideRequest,
    student_id: UUID = Depends(get_current_student_id),
    db: Session = Depends(get_db),
):
    try:
        return AdaptiveService.decide_next_action(db, student_id, body.topic_id, body.session_id)
    except LookupError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error