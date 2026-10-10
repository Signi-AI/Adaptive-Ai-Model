import os
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

# 1. CALCULATE POTENTIAL ROOT LOCATIONS
_current_file_dir = os.path.dirname(os.path.abspath(__file__))

# Option A: If running from project root (three levels up)
_root_option = os.path.abspath(os.path.join(_current_file_dir, "..", "..", "..", ".env"))

# Option B: If running from the backend directory (two levels up)
_backend_option = os.path.abspath(os.path.join(_current_file_dir, "..", "..", ".env"))

class Settings(BaseSettings):
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str
    # ... keep any other settings parameters exactly as you have them here ...

    PROJECT_NAME: str = "Adaptive AI Model"
    VERSION: str = "0.001"

    refresh_token_expire_days: int = 14
    access_token_expire_minutes: int = 30 
    # 2. PROVIDE AN ARRAY OF FALLBACKS
    model_config = SettingsConfigDict(
        # Pydantic checks these in order; the first file found wins!
        env_file=[_root_option, _backend_option],
        env_file_encoding="utf-8",
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()

