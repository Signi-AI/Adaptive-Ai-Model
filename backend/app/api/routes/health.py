"""
api/routes/health.py

Simple liveness check. Its only job is to prove the server is up and
answering requests - it deliberately does NOT touch the database, so
it can never fail because of a database problem. That's on purpose:
if /health is ever red, the problem is the process itself, not SQLite.
"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict:
    return {"status": "ok"}
