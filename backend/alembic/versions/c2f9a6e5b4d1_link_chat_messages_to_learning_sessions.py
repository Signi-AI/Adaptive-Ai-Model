"""Link chat history to the learning session that produced it.

Revision ID: c2f9a6e5b4d1
Revises: 8116aa579371
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.models.attempt import Attempt


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
    # The original baseline migration accidentally omitted the attempts table.
    # A clean deployment (such as Render's PostgreSQL database) therefore
    # reached this revision and failed while trying to ALTER a table that did
    # not exist.  Create the complete table from the registered model on a
    # fresh database; older databases retain their existing table and receive
    # only the new idempotency column below.
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "attempts" not in inspector.get_table_names():
        Attempt.__table__.create(bind, checkfirst=True)
    else:
        attempt_columns = {
            column["name"] for column in inspector.get_columns("attempts")
        }
        if "client_submission_id" not in attempt_columns:
            op.add_column(
                "attempts",
                sa.Column("client_submission_id", sa.UUID(), nullable=True),
            )

    attempt_indexes = {
        index["name"] for index in sa.inspect(bind).get_indexes("attempts")
    }
    if "uq_attempts_student_client_submission_id" not in attempt_indexes:
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
