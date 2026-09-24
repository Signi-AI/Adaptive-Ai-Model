from fastapi import APIRouter

from app.api.routes import health

api_router = APIRouter()

api_router.include_router(health.router)

# Example for whoever picks up the next route module:
# from app.api.routes import students
# api_router.include_router(students.router, prefix="/students", tags=["students"])