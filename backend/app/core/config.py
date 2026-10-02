"""
Centralized application configuration.

Every value is read from environment variables (or a local .env file
during development). Nothing here is hard-coded — the Student domain
issue explicitly forbids hard-coded secrets, and this is the one place
that changes between a school's lab server and any other machine.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # --- Database ---
    # postgresql+asyncpg://user:password@host:5432/dbname
    # "host" is the lab server's LAN address (or "localhost" if the API
    # and the database run on the same machine) — never a public one.
    database_url: str

    # --- JWT ---
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 14

    # --- App ---
    environment: str = "development"


@lru_cache
def get_settings() -> Settings:
    """
    Settings are constructed once and cached. FastAPI dependencies and
    other modules should call this function rather than instantiate
    Settings() directly, so tests can override it cleanly.
    """
    return Settings()
