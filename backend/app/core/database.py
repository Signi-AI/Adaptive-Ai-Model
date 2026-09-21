"""
core/database.py

The ONLY place in the project allowed to create a database connection.

Every other module (models, services, routes) must import from here:

    from app.core.database import Base, get_db

Do not call `create_engine` anywhere else. That is how "multiple
database connection patterns" (explicitly forbidden in this issue)
happen by accident on a team project.
"""

from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import MetaData, create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# SQLAlchemy's own recommended convention for deterministic constraint
# names (https://docs.sqlalchemy.org/en/20/core/constraints.html#configuring-a-naming-convention-for-a-metadata-collection).
# Without this, constraints (foreign keys especially) get no name at
# all on SQLite, and Alembic's autogenerate can't reference them when
# writing a downgrade() - the first migration that needs to drop or
# alter one (see the lesson_id column added to learning_sessions)
# generates a downgrade() that's guaranteed to fail on `alembic
# downgrade`, since there's no name to give drop_constraint(). This
# doesn't rename constraints on tables created by earlier migrations -
# only affects DDL SQLAlchemy emits from this point forward.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


def _ensure_sqlite_directory_exists(database_url: str) -> None:
    """
    SQLite will NOT create missing parent directories for you — it just
    fails with 'unable to open database file'. Since DATABASE_URL is
    something like 'sqlite:///./data/app.db', we pull the filesystem
    path back out and make sure ./data/ exists before SQLAlchemy ever
    tries to open a connection.
    """
    if not database_url.startswith("sqlite:///"):
        return  # not SQLite (e.g. a future Postgres URL) - nothing to do

    raw_path = database_url.replace("sqlite:///", "", 1)
    db_file = Path(raw_path)
    db_file.parent.mkdir(parents=True, exist_ok=True)


_ensure_sqlite_directory_exists(settings.DATABASE_URL)

# check_same_thread=False is required for SQLite specifically: FastAPI
# can serve one request per thread, but a single SQLite connection is
# opened on one thread by default and refuses to talk to any other
# thread unless we disable that check. This is safe here because each
# request gets its own Session (see get_db below).
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
)


@event.listens_for(engine, "connect")
def _enable_sqlite_foreign_keys(dbapi_connection, connection_record) -> None:
    """
    SQLite does NOT enforce foreign key constraints by default, even
    though ForeignKey(..., ondelete="CASCADE") is declared on a model
    - it silently accepts a Topic with a subject_id that doesn't
    exist unless this pragma is turned on for every connection.
    SQLAlchemy's own relationship(cascade=...) still works fine
    without this (it's Python-side), but this pragma is what stops
    bad data getting in from outside the ORM (raw SQL, a bug that
    skips the ORM layer, etc.) and is what makes ON DELETE CASCADE
    actually happen at the database level.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """
    Shared declarative base. Every SQLAlchemy model anyone on the team
    writes (student.py, subject.py, attempt.py, ...) must inherit from
    this exact class AND be imported in alembic/env.py, or
    `alembic revision --autogenerate` will never see it and will
    silently skip generating a migration for its table.
    """
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


BACKEND_DIR = Path(__file__).resolve().parents[2]  # app/core/database.py -> app/core -> app -> backend
ALEMBIC_INI_PATH = BACKEND_DIR / "alembic.ini"


def init_db() -> None:
    """
    Bring the database up to the latest Alembic migration (alembic
    upgrade head), called once at app startup (see app/main.py).

    This intentionally does NOT call Base.metadata.create_all(). Once
    Alembic owns the schema, create_all() must never run anywhere -
    if it created a table Alembic doesn't know about, the next
    `alembic upgrade head` (locally or in CI) would crash with
    "table already exists" instead of applying a clean migration.
    Alembic is now the single door into schema changes; this is the
    only place that door gets opened automatically.

    Safe to call repeatedly - upgrading to a revision you're already
    at is a no-op.
    """
    alembic_cfg = Config(str(ALEMBIC_INI_PATH))
    command.upgrade(alembic_cfg, "head")


def get_db():
    """
    FastAPI dependency that hands a route a database session and
    guarantees it gets closed afterwards, even if the route raises.

    Usage in a route:

        from fastapi import Depends
        from app.core.database import get_db

        @router.get("/something")
        def handler(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()