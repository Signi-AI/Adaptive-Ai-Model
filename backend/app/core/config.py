"""
core/config.py

Single source of truth for configuration.

Rule for the whole team: nobody reads os.environ directly anywhere else
in the codebase. If a module needs a setting, it imports `settings`
from this file. That keeps every configuration value in one place and
means changing an env var name only requires editing this file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Where values come from, in order of priority (highest first):
    #   1. real environment variables (e.g. exported in the shell / CI)
    #   2. a local .env file (copied from .env.example, git-ignored)
    #   3. the defaults below
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- App metadata -----------------------------------------------------
    PROJECT_NAME: str = "TOALM V2 - Artificial Teacher"
    VERSION: str = "0.1.0"
    DEBUG: bool = True

    # --- Database -----------------------------------------------------
    # SQLAlchemy connection string. Must stay a *relative* sqlite path
    # (sqlite:///./data/app.db) so the whole project keeps working with
    # zero internet connection and with no server to install, per the
    # offline requirement in the architecture doc.
    DATABASE_URL: str = "sqlite:///./data/app.db"


# One instance, imported everywhere else as `from app.core.config import settings`.
settings = Settings()
