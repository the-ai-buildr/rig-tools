"""
Configuration for Well Dashboard API

All settings are read from environment variables, with safe defaults for local development.
Set these via docker-compose.yml, a .env file, or the shell environment before running.

Usage:
    from api.config import settings
    print(settings.DATABASE_PATH)
"""

import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings — sourced from environment variables."""

    # ── API Server ────────────────────────────────────────────────────────────
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False

    # ── Database ──────────────────────────────────────────────────────────────
    DATABASE_PATH: str = "/app/db/well_database.db"

    # ── File Paths ────────────────────────────────────────────────────────────
    EXPORT_PATH: str = "/app/exports"
    TEMPLATE_PATH: str = "/app/templates"

    # ── Security ──────────────────────────────────────────────────────────────
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # ── CORS ─────────────────────────────────────────────────────────────────
    CORS_ORIGINS: list = ["*"]  # Restrict in production

    # ── Streamlit (informational) ─────────────────────────────────────────────
    STREAMLIT_PORT: int = 8501

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton settings instance — import this everywhere
settings = Settings()


def ensure_directories() -> None:
    """Create all required runtime directories if they don't already exist."""
    dirs = [
        settings.EXPORT_PATH,
        settings.TEMPLATE_PATH,
        os.path.dirname(settings.DATABASE_PATH),
    ]
    for path in dirs:
        os.makedirs(path, exist_ok=True)
