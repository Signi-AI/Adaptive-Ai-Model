"""
Pydantic schemas for the AI Teaching Session chat (MVP placeholder version).
"""
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.chat_message import ChatRole


class ChatMessageRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)


class ChatMessagePublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    role: ChatRole
    content: str
    created_at: datetime


class ChatReplyResponse(BaseModel):
    student_message: ChatMessagePublic
    ai_reply: ChatMessagePublic
