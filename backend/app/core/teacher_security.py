"""
Teacher access-token creation.

This is NOT a second JWT system. It signs with the same secret, algorithm and
lifetime from app.core.config, produces the same token shape (type="access"),
and is validated by the same shared app.core.security.decode_access_token.
The only addition is a "role" claim, which is what lets teacher-only routes
reject a perfectly valid *student* token.
"""
from datetime import datetime, timedelta, timezone


import jwt
from app.core.config import get_settings
from app.core.security import TokenType

TEACHER_ROLE = "TEACHER"




def create_teacher_access_token(teacher_id: str) -> tuple[str, datetime]:
    """Returns (token, expires_at_utc). No session_id claim: teachers have no
    student-session row, so this token is also useless on student endpoints."""
    settings = get_settings()
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": teacher_id,
        "role": TEACHER_ROLE,
        "type": TokenType.ACCESS.value,
        "iat": now,
        "exp": expires_at,
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token, expires_at
