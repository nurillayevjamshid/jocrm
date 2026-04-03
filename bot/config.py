"""
Bot Configuration - Simple and clean.
"""

from functools import lru_cache
from typing import List, Optional

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Bot settings from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Required
    BOT_TOKEN: str = Field(description="Telegram bot token from @BotFather")

    # Optional
    BOT_MODE: str = Field(default="polling")
    WEBHOOK_URL: Optional[str] = Field(default=None)
    ADMIN_IDS: Optional[str] = Field(default=None)
    
    # MiniApp URL - set to your Netlify URL for production
    # Example: https://forever-crm-miniapp.netlify.app
    MINIAPP_URL: str = Field(default="http://localhost:5173")
    
    DEBUG: bool = Field(default=False)
    LOG_LEVEL: str = Field(default="INFO")

    @computed_field
    @property
    def admin_ids_list(self) -> List[int]:
        """Parse admin IDs from comma-separated string."""
        if not self.ADMIN_IDS:
            return []
        return [int(x.strip()) for x in self.ADMIN_IDS.split(",") if x.strip().isdigit()]


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
