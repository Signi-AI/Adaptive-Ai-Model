"""Link chat history to the learning session that produced it.

Revision ID: c2f9a6e5b4d1
Revises: 8116aa579371
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c2f9a6e5b4d1"
down_revision: Union[str, Sequence[str], None] = "8116aa579371"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("chat_messages", sa.Column("learning_session_id", sa.UUID(), nullable=True))
    op.create_foreign_key(
        "fk_chat_messages_learning_session_id_learning_sessions",
        "chat_messages",
        "learning_sessions",
        ["learning_session_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.create_index("ix_chat_messages_learning_session_id", "chat_messages", ["learning_session_id"])
    op.add_column("attempts", sa.Column("client_submission_id", sa.UUID(), nullable=True))
    op.create_index(
        "uq_attempts_student_client_submission_id",
        "attempts",
        ["student_id", "client_submission_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("uq_attempts_student_client_submission_id", table_name="attempts")
    op.drop_column("attempts", "client_submission_id")
    op.drop_index("ix_chat_messages_learning_session_id", table_name="chat_messages")
    op.drop_constraint("fk_chat_messages_learning_session_id_learning_sessions", "chat_messages", type_="foreignkey")
    op.drop_column("chat_messages", "learning_session_id")
