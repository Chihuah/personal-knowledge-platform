from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "Personal Knowledge Platform API"
    app_version: str = "0.1.0"
    app_env: str = Field(default="development", alias="BACKEND_APP_ENV")
    log_level: str = Field(default="INFO", alias="BACKEND_LOG_LEVEL")
    host: str = Field(default="0.0.0.0", alias="BACKEND_HOST")
    port: int = Field(default=8000, alias="BACKEND_PORT")
    database_url: str = Field(
        default="postgresql+psycopg://pkp:pkp@postgres:5432/pkp",
        alias="DATABASE_URL",
    )
    redis_url: str = Field(default="redis://redis:6379/0", alias="REDIS_URL")
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4.1-mini", alias="OPENAI_MODEL")
    tasks_mode: str = Field(default="inline", alias="TASKS_MODE")
    celery_task_always_eager: bool = Field(
        default=False,
        alias="CELERY_TASK_ALWAYS_EAGER",
    )
    parser_timeout_seconds: int = Field(default=20, alias="PARSER_TIMEOUT_SECONDS")
    items_page_size_default: int = Field(default=20, alias="ITEMS_PAGE_SIZE_DEFAULT")
    items_page_size_max: int = Field(default=100, alias="ITEMS_PAGE_SIZE_MAX")
    cors_origins_raw: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000",
        alias="BACKEND_CORS_ORIGINS",
    )

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin in self.cors_origins_raw.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    return Settings()
