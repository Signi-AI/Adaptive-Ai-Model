"""
Security primitives for the Student domain: password hashing and JWT
access/refresh token handling.

Design choices — read before changing anything here:

- Passwords are hashed with Argon2id (via passlib), the current OWASP
  recommendation. Argon2 is memory-hard, which matters because this app
  runs on ordinary school lab hardware shared by many students — it
  resists offline cracking even if the database is ever copied off the
  server.

- Access tokens are short-lived, stateless JWTs (HS256). They are not
  validated by signature alone: every access token carries a session_id,
  and app/api/deps.py checks that the referenced session is still active
  on every request. This is deliberate — on a shared lab PC, a student
  who logs out must be denied immediately, not just once their token
  happens to expire on its own.

- Refresh tokens are opaque random strings, not JWTs. Only a SHA-256
  hash of the refresh token is ever stored in the database (see
  models/student.py::StudentSession.refresh_token_hash). SHA-256 — not
  Argon2 — is used here on purpose: refresh tokens are already
  high-entropy random values, not human-chosen passwords, so a slow
  password hash would only add CPU cost on every refresh request without
  adding real security. This follows the issue's instruction not to
  store sensitive tokens as plaintext.

- Refresh tokens rotate on every use (see
  services/student_service.py::refresh_session): each call to
  /auth/refresh invalidates the presented refresh token and issues a new
  one. This makes stolen-token replay detectable — if an attacker's
  copy is used after the legitimate one has already rotated, the lookup
  fails and the whole session can be treated as compromised.
"""
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from enum import Enum
from typing import Any

import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()

_pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# --------------------------------------------------------------------------
# Password hashing
# --------------------------------------------------------------------------

def hash_password(plain_password: str) -> str:
    return _pwd_context.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return _pwd_context.verify(plain_password, password_hash)


# --------------------------------------------------------------------------
# JWT access tokens
# --------------------------------------------------------------------------

class TokenType(str, Enum):
    ACCESS = "access"


def create_access_token(*, student_id: str, session_id: str) -> tuple[str, datetime]:
    """Returns (token, expires_at_utc)."""
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=settings.access_token_expire_minutes)

    payload: dict[str, Any] = {
        "sub": student_id,
        "session_id": session_id,
        "type": TokenType.ACCESS.value,
        "iat": now,
        "exp": expires_at,
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token, expires_at


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Raises a jwt.InvalidTokenError subclass if the token is malformed,
    expired, or was not issued as an access token. Callers (see
    api/deps.py) turn that into an HTTP 401.
    """
    payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    if payload.get("type") != TokenType.ACCESS.value:
        raise jwt.InvalidTokenError("Not an access token")
    return payload


# --------------------------------------------------------------------------
# Opaque refresh tokens
# --------------------------------------------------------------------------

def generate_refresh_token() -> str:
    """A high-entropy, URL-safe random string — deliberately not a JWT."""
    return secrets.token_urlsafe(48)


def hash_refresh_token(raw_token: str) -> str:
    return hashlib.sha256(raw_token.encode("utf-8")).hexdigest()


def refresh_token_expiry() -> datetime:
    return datetime.now(timezone.utc) + timedelta(days=settings.refresh_token_expire_days)
