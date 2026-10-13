"""
Shared field-level validation/normalization for the Teacher domain.

Used from TWO places on purpose:
  - schemas/teacher.py's Pydantic field_validators (API request bodies)
  - services/teacher_service.py, specifically create_teacher() (called
    directly by scripts/seed_teacher_dev.py and tests, which never go
    through a Pydantic model at all -- there is no public registration
    endpoint, so this was the only path that previously had NO validation)

Every function here raises plain ValueError on invalid input and returns the
cleaned value on success -- nothing FastAPI/Pydantic-specific. A Pydantic
field_validator can call one directly (Pydantic turns ValueError into a 422
automatically). Service-layer code must catch ValueError itself and translate
it into whatever HTTPException fits that call site -- see create_teacher().
"""
import re

_PHONE_PATTERN = re.compile(r"^\+?[0-9 ()\-]{6,32}$")


def clean_email(value: str) -> str:
    """Strips and does a minimal sanity check. Full RFC validation is
    deliberately not attempted -- Teacher.email uniqueness is enforced
    case-insensitively at the database level regardless."""
    value = value.strip()
    if not value or "@" not in value or value.startswith("@") or value.endswith("@"):
        raise ValueError("email must be a valid email address")
    return value


def clean_full_name(value: str | None) -> str:
    """Strips and enforces a minimum length. Raises on None or too-short."""
    if value is None:
        raise ValueError("full_name cannot be null")
    value = value.strip()
    if len(value) < 2:
        raise ValueError("full_name must be at least 2 characters")
    return value


def clean_optional_phone(value: str | None) -> str | None:
    """Strips; treats "" as None (clears the field); validates format otherwise."""
    if value is None:
        return None
    value = value.strip()
    if value == "":
        return None
    if not _PHONE_PATTERN.match(value):
        raise ValueError("phone_number must be 6-32 characters: digits, spaces, + ( ) -")
    return value


def clean_optional_text(value: str | None) -> str | None:
    """Generic strip; treats "" as None. Used for specialization, subject, topic."""
    if value is None:
        return None
    value = value.strip()
    return value or None


def clean_required_text(value: str, *, field_name: str = "value") -> str:
    """Strips and rejects blank. Used for guidance_text."""
    value = value.strip()
    if not value:
        raise ValueError(f"{field_name} cannot be blank")
    return value


def role_name_from_value(value):
    """
    Pydantic `field_validator(mode="before")` helper for any `role: UserRole`
    response field. User.role / UserSession.role are now relationships to a
    Role ORM row (see models/role.py), not a plain enum value -- this
    extracts .name if given an ORM object, and passes plain strings/enums
    through unchanged. Keeps every external API response shaped exactly as
    "role": "STUDENT" regardless of how storage is implemented underneath.
    """
    return value.name if hasattr(value, "name") else value
