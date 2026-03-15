from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    # Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = False

    # Security
    secret_key: str = "change-this-secret-key-in-production"
    access_token_expire_minutes: int = 1440  # 24 hours

    # CORS — lock down in production
    cors_origins: list[str] = ["*"]

    # Paths (volume-mounted in Docker)
    data_path: str = "/app/data"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()


def ensure_directories() -> None:
    Path(settings.data_path).mkdir(parents=True, exist_ok=True)
