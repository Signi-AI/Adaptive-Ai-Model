"""
SQLAlchemy engine/session setup for the shared PostgreSQL server.

One engine is created per process (the FastAPI app running on the
school/lab server). Every request gets its own Session via the
get_db dependency in app/api/deps.py — sessions are never shared across
concurrent requests, which matters here specifically because many
students may be hitting this one server at once.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,  # detect connections the DB dropped (e.g. after a restart)
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Shared declarative base for every ORM model in the app."""
    pass


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
