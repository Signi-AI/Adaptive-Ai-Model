"""
Shared pytest fixtures for the Student domain tests.

These tests expect a real PostgreSQL instance reachable via
TEST_DATABASE_URL (falls back to a local default). They create and drop
the students/student_sessions tables directly around the test session,
so `pytest` alone exercises the domain's logic. That's deliberately
separate from actually proving "migrations work from a clean database"
(the DoD's own wording) — do that by running
`alembic upgrade head` against a throwaway database, see
README_STUDENT_DOMAIN.md.
"""
import os
import uuid

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql://toalm_user:change_me@localhost:5432/toalm_test",
)
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-not-for-production")

from backend.app.core.database import Base, engine  # noqa: E402
from backend.app.main import app  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _create_schema():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def _clean_tables():
    yield
    with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


def unique_username() -> str:
    return f"student_{uuid.uuid4().hex[:10]}"
