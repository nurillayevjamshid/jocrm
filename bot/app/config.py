"""
Bot Service Configuration.

Manages environment variables for the Telegram bot entry point.
"""

from functools import lru_cache
from typing import List, Optional

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Bot service settings."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
    # Bot Configuration
    BOT_TOKEN: str = Field(description="Telegram bot token")
    BOT_MODE: str = Field(default="polling")
    WEBHOOK_URL: Optional[str] = Field(default=None)
    WEBHOOK_SECRET: Optional[str] = Field(default=None)
    
    # Admin Settings
    ADMIN_IDS: Optional[str] = Field(default=None)
    SUPER_ADMIN_ID: Optional[int] = Field(default=None)
    
    # URLs for Mini App
    API_URL: str = Field(default="http://localhost:8000")
    MINIAPP_URL: str = Field(default="https://your-mini-app-url.com")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO")
    DEBUG: bool = Field(default=False)
    
    @computed_field
    @property
    def admin_ids_list(self) -> List[int]:
        """Parse admin IDs from comma-separated string."""
        if not self.ADMIN_IDS:
            return []
        return [
            int(x.strip())
            for x in self.ADMIN_IDS.split(",")
            if x.strip().isdigit()
        ]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
