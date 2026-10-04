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

from app.api.router import api_router
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.services import role_service


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


