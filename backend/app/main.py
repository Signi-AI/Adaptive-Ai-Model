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
from app.core.config import settings
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    # Guarantee the SQLite file and every currently-registered table
    # exist before the app accepts its first request.
    init_db()
    yield
    # --- Shutdown ---
    # Nothing to clean up yet. SQLite needs no explicit disconnect step.


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
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

app.include_router(api_router)

