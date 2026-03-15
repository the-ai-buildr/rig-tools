"""
Application settings — all environment variables are read here.
No credentials are hardcoded; all sensitive values come from docker/.env or env.

Produced by: backend-agent / fastapi-routes skill
"""
from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # Server
    debug: bool = False

    # Security
    secret_key: str = "change-this-secret-key-in-production"
    access_token_expire_minutes: int = 1440  # 24 hours

    # CORS — lock down in production
    cors_origins: list[str] = ["*"]

    # Paths (volume-mounted in Docker)
    data_path: str = "/app/data"

    # Streamlit + FastAPI share the same process on the same port (8501).
    # Override only when calling from outside the container.
    api_base_url: str = "http://localhost:8501"

    # Supabase
    supabase_url: str = ""
    supabase_anon_key: str = ""
    supabase_service_role_key: str = ""

    # Supabase CLI — used only by migration tooling, not at runtime
    supabase_db_url: str = ""
    supabase_project_ref: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}

    def validate_production_secrets(self) -> None:
        """Raise at startup if placeholder secrets are used outside debug mode."""
        if not self.debug and self.secret_key == "change-this-secret-key-in-production":
            raise RuntimeError(
                "SECRET_KEY must be changed from the default before running in production. "
                "Set it in docker/.env."
            )


settings = Settings()


def ensure_directories() -> None:
    Path(settings.data_path).mkdir(parents=True, exist_ok=True)
