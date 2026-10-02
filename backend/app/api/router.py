from fastapi import APIRouter

from app.api.routes import admin, auth, learning, students, teacher
from backend.app.api.routes import sessions
from backend.app.main import health

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(students.router)
api_router.include_router(learning.router)
api_router.include_router(teacher.router)
api_router.include_router(admin.router)

# NOTE: your live project also has health.py and sessions.py (referenced in
# the router.py you pasted earlier) that were never shared with me. This
# rewrite's session endpoints live inside students.py / teacher.py, as they
# always have in what I've delivered -- if your sessions.py contains custom
# changes beyond that, you'll need to port them in yourself, since I have no
# visibility into that file's contents. health.py is unrelated to identity
# and untouched by anything in this change -- just include it as before.

api_router.include_router(health.router)
api_router.include_router(sessions.router)