"""
Business logic for the AI Teaching Session chat (MVP placeholder version).

post_chat_message stores the student's message and immediately generates
a placeholder AI reply -- no curriculum context, no Gemma call yet. This
gives the frontend a real, working endpoint to build against while the
curriculum domain and Gemma client don't exist yet. When those exist,
only _generate_placeholder_reply needs replacing with a real call into
an AI Teacher Service (docs Section 31) -- the storage shape stays valid.
"""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage, ChatRole


def _generate_placeholder_reply(student_message: str) -> str:
    return (
        "Thanks for your message! I received it: "
        f'"{student_message.strip()}". '
        "The full Artificial Teacher isn't wired in yet -- this is a "
        "placeholder reply so the chat flow can be tested end to end."
    )


def post_chat_message(
    db: Session, student_id: uuid.UUID, message: str
) -> tuple[ChatMessage, ChatMessage]:
    student_row = ChatMessage(student_id=student_id, role=ChatRole.STUDENT, content=message)
    db.add(student_row)
    db.flush()  # assigns id/created_at before commit, and before building the reply

    reply_text = _generate_placeholder_reply(message)
    reply_row = ChatMessage(student_id=student_id, role=ChatRole.AI_TEACHER, content=reply_text)
    db.add(reply_row)

    db.commit()
    db.refresh(student_row)
    db.refresh(reply_row)
    return student_row, reply_row


def get_chat_history(db: Session, student_id: uuid.UUID) -> list[ChatMessage]:
    result = db.execute(
        select(ChatMessage)
        .where(ChatMessage.student_id == student_id)
        .order_by(ChatMessage.created_at.asc())
    )
    return list(result.scalars().all())
