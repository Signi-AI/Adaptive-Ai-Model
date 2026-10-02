"""
POST /learning/session/message
GET  /learning/session/messages
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_student, get_db
from app.models.user import User
from app.schemas.learning import ChatMessagePublic, ChatMessageRequest, ChatReplyResponse
from app.services import learning_service

router = APIRouter(prefix="/learning", tags=["learning"])


@router.post("/session/message", response_model=ChatReplyResponse)
def post_message(
    payload: ChatMessageRequest,
    current_student: User = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    student_row, reply_row = learning_service.post_chat_message(
        db, current_student.id, payload.message
    )
    return ChatReplyResponse(
        student_message=ChatMessagePublic.model_validate(student_row),
        ai_reply=ChatMessagePublic.model_validate(reply_row),
    )


@router.get("/session/messages", response_model=list[ChatMessagePublic])
def get_messages(
    current_student: User = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    return learning_service.get_chat_history(db, current_student.id)
