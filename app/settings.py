import secrets

from typing import Any, Literal
from pathlib import Path
from pydantic import (
    HttpUrl,
    PostgresDsn,
    computed_field,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    ENVIRONMENT: Literal["local", "staging", "production"] = "local"

    PROJECT_NAME: str = "Task Management API"
    SENTRY_DSN: HttpUrl | None = None
    POSTGRES_SERVER: str = ""
    POSTGRES_PORT: int
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    EMAILS_FROM_NAME: str = "noreply@taskmanagement.com"
    EMAILS_FROM_EMAIL: str = ""
    SMTP_HOST: str = ""
    SMTP_USER: str = "vumichael0811@gmail.com"
    SMTP_PASSWORD: str = ""
    SMTP_TLS: bool
    SMTP_SSL: bool
    SMTP_PORT: int = 587

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()  # type: ignore
