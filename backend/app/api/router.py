"""
api/router.py

The single shared router main.py mounts onto the app.

Everyone else's future routes (students.py, learning.py, assessments.py,
progress.py, recommendations.py, teacher.py) get wired in HERE with one
extra `api_router.include_router(...)` line each - main.py itself
should never need to change again once this issue lands.
"""

from fastapi import APIRouter

from app.api.routes import health, learning, sessions, students

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(students.router)
api_router.include_router(learning.router)
api_router.include_router(sessions.router)