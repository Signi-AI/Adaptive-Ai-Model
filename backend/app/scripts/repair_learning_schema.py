"""Repair the learning integration schema on databases created before this feature.

This is safe to run repeatedly.  It is intentionally narrow: it creates only
the missing ``attempts`` table, adds ``chat_messages.learning_session_id``,
and advances Alembic's revision after the schema is confirmed.

Run from ``backend``:
    python -m app.scripts.repair_learning_schema
"""
from __future__ import annotations

from sqlalchemy import inspect, text

from app.core.database import engine
from app.models.attempt import Attempt

REVISION = "c2f9a6e5b4d1"


def main() -> None:
    with engine.begin() as connection:
        inspector = inspect(connection)
        chat_columns = {column["name"] for column in inspector.get_columns("chat_messages")}
        if "learning_session_id" not in chat_columns:
            connection.execute(text("ALTER TABLE chat_messages ADD COLUMN learning_session_id UUID"))
            connection.execute(text(
                "ALTER TABLE chat_messages ADD CONSTRAINT "
                "fk_chat_messages_learning_session_id_learning_sessions "
                "FOREIGN KEY (learning_session_id) REFERENCES learning_sessions(id) ON DELETE SET NULL"
            ))
            connection.execute(text(
                "CREATE INDEX ix_chat_messages_learning_session_id "
                "ON chat_messages (learning_session_id)"
            ))
            print("added chat_messages.learning_session_id")

        if "attempts" not in inspector.get_table_names():
            Attempt.__table__.create(connection, checkfirst=True)
            print("created attempts table")

        attempt_columns = {column["name"] for column in inspect(connection).get_columns("attempts")}
        if "client_submission_id" not in attempt_columns:
            connection.execute(text("ALTER TABLE attempts ADD COLUMN client_submission_id UUID"))
            print("added attempts.client_submission_id")

        connection.execute(text(
            "CREATE UNIQUE INDEX IF NOT EXISTS uq_attempts_student_client_submission_id "
            "ON attempts (student_id, client_submission_id)"
        ))
        connection.execute(text("UPDATE alembic_version SET version_num = :revision"), {"revision": REVISION})

    print(f"Learning schema is ready at migration {REVISION}.")


if __name__ == "__main__":
    main()
