"""
POST /learning/session/message
GET  /learning/session/messages
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_student, get_db
from app.models.user import User
from app.ai.model_client import TeacherModelError
from app.schemas.learning import (
    ChatMessagePublic,
    ChatMessageRequest,
    ChatReplyResponse,
    LearningSessionPublic,
    LearningSessionRequest,
    AttemptSubmissionRequest,
    AttemptSubmissionResponse,
    PracticeQuestionPublic,
)
from app.services import learning_service

router = APIRouter(prefix="/learning", tags=["learning"])


@router.post("/session/message", response_model=ChatReplyResponse)
def post_message(
    payload: ChatMessageRequest,
    current_student: User = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    try:
        student_row, reply_row = learning_service.post_chat_message(
            db, current_student, payload.session_id, payload.message
        )
    except TeacherModelError as error:
        raise HTTPException(status_code=error.status_code, detail=str(error)) from error
    except LookupError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
    return ChatReplyResponse(
        session_id=payload.session_id,
        student_message=ChatMessagePublic.model_validate(student_row),
        ai_reply=ChatMessagePublic.model_validate(reply_row),
    )


@router.post("/sessions", response_model=LearningSessionPublic, status_code=status.HTTP_201_CREATED)
def create_session(
    payload: LearningSessionRequest,
    current_student: User = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    try:
        return learning_service.start_session(
            db, current_student.id, payload.subject_id, payload.topic_id, payload.lesson_id
        )
    except LookupError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error


@router.get("/session/messages", response_model=list[ChatMessagePublic])
def get_messages(
    session_id: str,
    current_student: User = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    try:
        from uuid import UUID
        return learning_service.get_chat_history(db, current_student.id, UUID(session_id))
    except (LookupError, ValueError) as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning session not found") from error


@router.get("/sessions/{session_id}/question", response_model=PracticeQuestionPublic)
def get_practice_question(
    session_id: str,
    current_student: User = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    try:
        from uuid import UUID
        question = learning_service.get_practice_question(db, current_student.id, UUID(session_id))
        return PracticeQuestionPublic(id=question.id, text=question.generated_text)
    except (LookupError, ValueError) as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@router.post("/attempts", response_model=AttemptSubmissionResponse)
def submit_attempt(
    payload: AttemptSubmissionRequest,
    current_student: User = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    try:
        attempt, learning_state, decision, recommendations = learning_service.submit_attempt(
            db,
            current_student.id,
            payload.session_id,
            payload.question_id,
            payload.student_answer,
            payload.client_submission_id,
        )
    except LookupError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)) from error
    if decision is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Attempt is still being processed")
    return AttemptSubmissionResponse(
        attempt_id=attempt.id,
        is_correct=attempt.is_correct,
        score=attempt.score,
        feedback=attempt.ai_feedback or "Answer recorded.",
        mastery_score=learning_state.mastery_score,
        next_action=decision.action.value,
        recommendation_count=len(recommendations),
    )
