"""
Backend Configuration - Simple and clean.
"""

from functools import lru_cache
from typing import List, Optional

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Backend settings from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Server
    API_HOST: str = Field(default="0.0.0.0")
    API_PORT: int = Field(default=8000)

    # CORS
    CORS_ORIGINS: str = Field(default="http://localhost:5173")

    # Database
    DATABASE_URL: Optional[str] = Field(default=None)
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5432)
    DB_NAME: str = Field(default="crm_db")
    DB_USER: str = Field(default="postgres")
    DB_PASSWORD: str = Field(default="")

    # Redis
    REDIS_URL: Optional[str] = Field(default=None)

    # Security
    SECRET_KEY: str = Field(default="your-secret-key")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)

    # Telegram
    BOT_TOKEN: Optional[str] = Field(default=None)

    # Feature Flags
    DEBUG: bool = Field(default=False)
    LOG_LEVEL: str = Field(default="INFO")
    ENABLE_SWAGGER: bool = Field(default=True)

    @computed_field
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [x.strip() for x in self.CORS_ORIGINS.split(",")]

    @computed_field
    @property
    def database_url(self) -> str:
        """Get database URL or build from params."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
