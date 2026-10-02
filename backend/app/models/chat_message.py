"""
ORM model for the AI Teaching Session chat log (MVP placeholder version).

Each turn is two rows: one STUDENT row, one AI_TEACHER row. This shape
doesn't need to change once the real orchestration (docs Section 31-33)
replaces the placeholder reply with an actual Gemma call -- only
learning_service.py's reply-generation changes.

student_id now points at users.id (the unified identity table) instead of a
separate students table. The column keeps its old name -- it still means
"the student this message belongs to" -- only the table it references
changed. If that student is later promoted to a teacher, their prior chat
history is deleted as part of "erase and start over" (see
services/user_service.py::promote_to_teacher); it never becomes orphaned or
reassigned to their new teacher identity.
"""
import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Text, func
from sqlalchemy import Enum as PgEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ChatRole(str, Enum):
    STUDENT = "STUDENT"
    AI_TEACHER = "AI_TEACHER"


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    role: Mapped[ChatRole] = mapped_column(PgEnum(ChatRole, name="chat_role"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
