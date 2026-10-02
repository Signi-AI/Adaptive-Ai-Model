"""
main.py

Application entry point. Run with:

    uvicorn app.main:app --reload

Keep this file thin. It should only ever wire things together
(settings -> app -> middleware -> router -> startup). Actual logic
belongs in core/, api/, services/, etc. - not here.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.student_curriculum import router as student_curriculum_router
from app.api.academic_levels import router as academic_levels_router
from app.api.curriculum import router as curriculum_router
from app.api.learning_objectives import router as learning_objectives_router
from app.api.lesson import router as lesson_router
from app.api.router import api_router
from app.core.config import get_settings
from app.api.routes import learning
#from app.core.database import init_db
from app.api.subjects import router as subjects_router
from app.api.topics import router as topics_router
from backend.app.core.database import SessionLocal
from backend.app.services import role_service
app= FastAPI(
    title="Artificial Teacher API",
)

app = FastAPI(
    title=get_settings().PROJECT_NAME,
    version=get_settings().VERSION
    #debug=get_settings().DEBUG
)

# Wide-open CORS for now: this is an offline, single-machine app during
# development and the frontend will likely run on a different local
# port (e.g. Vite on :5173 talking to FastAPI on :8000). Tighten
# allow_origins to the real frontend origin before this ever ships.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Guarantees the three roles exist the moment the app starts serving
    # requests -- ordinary student self-registration (and every login)
    # depends on a role row existing, so this cannot wait on someone
    # remembering to run a seed script first. Idempotent; safe on every
    # restart. The actual admin IDENTITY (real credentials) is deliberately
    # a separate, explicit step -- see scripts/seed_admin.py.
    with SessionLocal() as db:
        role_service.ensure_core_roles_exist(db)
    yield

app.include_router(api_router)
app.include_router(subjects_router)
app.include_router(topics_router)
app.include_router(lesson_router)
app.include_router(learning_objectives_router)
app.include_router(curriculum_router)
app.include_router(academic_levels_router)
app.include_router(student_curriculum_router)

@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
