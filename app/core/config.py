"""
Application configuration module.

Loads environment variables and provides typed settings for the application.
Uses pydantic-settings for validation, type safety, and computed properties.

Architecture:
    - Settings class: Central configuration container
    - get_settings(): Cached singleton accessor
    - Environment-based configuration with .env file support
    - Future-proof: Ready for Database, Redis, FastAPI integration
"""

from functools import lru_cache
from typing import List, Optional
from enum import Enum

from pydantic import Field, field_validator, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BotMode(str, Enum):
    """Bot operation modes."""
    POLLING = "polling"
    WEBHOOK = "webhook"


class LogLevel(str, Enum):
    """Logging levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Settings(BaseSettings):
    """
    Central application settings container.
    
    All configuration is loaded from environment variables with sensible defaults.
    Sections are organized by functionality for maintainability.
    
    Usage:
        from app.core.config import get_settings
        settings = get_settings()
        bot_token = settings.BOT_TOKEN
    """
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Allow extra env vars for forward compatibility
        str_strip_whitespace=True,
    )
    
    # ============================================================
    # SECTION 1: BOT CONFIGURATION (Required)
    # ============================================================
    
    BOT_TOKEN: str = Field(
        description="Telegram bot token from @BotFather"
    )
    
    BOT_MODE: BotMode = Field(
        default=BotMode.POLLING,
        description="Bot mode: polling (dev) or webhook (prod)"
    )
    
    WEBHOOK_URL: Optional[str] = Field(
        default=None,
        description="Webhook URL (required if BOT_MODE=webhook)"
    )
    
    WEBHOOK_SECRET: Optional[str] = Field(
        default=None,
        description="Secret token for webhook security"
    )
    
    # ============================================================
    # SECTION 2: ADMINISTRATION
    # ============================================================
    
    ADMIN_IDS: Optional[str] = Field(
        default=None,
        description="Comma-separated admin Telegram user IDs"
    )
    
    SUPER_ADMIN_ID: Optional[int] = Field(
        default=None,
        description="Super admin ID with full system access"
    )
    
    @computed_field
    @property
    def admin_ids_list(self) -> List[int]:
        """
        Parse ADMIN_IDS string into validated list of integers.
        
        Returns:
            List of admin user IDs, empty list if ADMIN_IDS not set
        """
        if not self.ADMIN_IDS:
            return []
        return [
            int(admin_id.strip())
            for admin_id in self.ADMIN_IDS.split(",")
            if admin_id.strip().isdigit()
        ]
    
    @computed_field
    @property
    def is_admin_set(self) -> bool:
        """Check if any admin IDs are configured."""
        return len(self.admin_ids_list) > 0
    
    # ============================================================
    # SECTION 3: DATABASE (Stage 2 - PostgreSQL + SQLAlchemy)
    # ============================================================
    
    DATABASE_URL: Optional[str] = Field(
        default=None,
        description="Full PostgreSQL connection URL"
    )
    
    # Alternative: Individual connection parameters
    DB_HOST: str = Field(default="localhost")
    DB_PORT: int = Field(default=5432)
    DB_NAME: str = Field(default="crm_db")
    DB_USER: str = Field(default="postgres")
    DB_PASSWORD: str = Field(default="")
    
    # Connection pool settings
    DB_POOL_SIZE: int = Field(default=20)
    DB_MAX_OVERFLOW: int = Field(default=10)
    DB_POOL_TIMEOUT: int = Field(default=30)
    
    @computed_field
    @property
    def database_url_computed(self) -> Optional[str]:
        """
        Build DATABASE_URL from individual parameters if not provided.
        
        Priority:
            1. DATABASE_URL environment variable
            2. Built from DB_HOST, DB_PORT, etc.
        
        Returns:
            PostgreSQL async connection URL or None if DB not configured
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL
        if self.DB_PASSWORD:
            return (
                f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
                f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
            )
        return None
    
    @computed_field
    @property
    def is_database_configured(self) -> bool:
        """Check if database is properly configured."""
        return self.database_url_computed is not None
    
    # ============================================================
    # SECTION 4: REDIS / CACHE (Stage 2-3)
    # ============================================================
    
    REDIS_URL: Optional[str] = Field(
        default=None,
        description="Redis connection URL"
    )
    
    REDIS_CACHE_TTL: int = Field(
        default=3600,
        description="Default cache TTL in seconds"
    )
    
    @computed_field
    @property
    def is_redis_configured(self) -> bool:
        """Check if Redis is configured."""
        return self.REDIS_URL is not None
    
    # ============================================================
    # SECTION 5: WEB API (Stage 3 - FastAPI)
    # ============================================================
    
    API_HOST: str = Field(default="0.0.0.0")
    API_PORT: int = Field(default=8000)
    API_DOCS: bool = Field(default=True)
    API_SECRET_KEY: Optional[str] = Field(default=None)
    
    @computed_field
    @property
    def api_base_url(self) -> str:
        """Build API base URL."""
        return f"http://{self.API_HOST}:{self.API_PORT}"
    
    # ============================================================
    # SECTION 6: SECURITY & FEATURE FLAGS
    # ============================================================
    
    DEBUG: bool = Field(
        default=False,
        description="Debug mode - NEVER enable in production!"
    )
    
    LOG_LEVEL: LogLevel = Field(default=LogLevel.INFO)
    
    RATE_LIMIT_PER_MINUTE: int = Field(
        default=30,
        description="Max messages per minute per user"
    )
    
    @field_validator("DEBUG", mode="before")
    @classmethod
    def validate_debug(cls, v: bool) -> bool:
        """Warn if DEBUG is enabled."""
        if v:
            # In real app, use proper logging here
            print("⚠️  WARNING: DEBUG mode is enabled! Never use in production.")
        return v
    
    # ============================================================
    # SECTION 7: BUSINESS CONFIGURATION
    # ============================================================
    
    COMPANY_NAME: str = Field(default="For.Ever Cosmetics")
    COMPANY_PHONE: Optional[str] = Field(default=None)
    COMPANY_EMAIL: Optional[str] = Field(default=None)
    DEFAULT_CURRENCY: str = Field(default="UZS")
    TIMEZONE: str = Field(default="Asia/Tashkent")
    
    # ============================================================
    # COMPUTED PROPERTIES
    # ============================================================
    
    @computed_field
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.DEBUG
    
    @computed_field
    @property
    def is_webhook_mode(self) -> bool:
        """Check if bot is configured for webhook mode."""
        return self.BOT_MODE == BotMode.WEBHOOK


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached Settings singleton instance.
    
    Using lru_cache ensures:
        - .env file is loaded only once
        - Settings are validated only once
        - Memory efficient access across the application
    
    Returns:
        Settings: Validated application settings
    
    Example:
        >>> from app.core.config import get_settings
        >>> settings = get_settings()
        >>> print(settings.BOT_TOKEN)
    """
    return Settings()


# Export for convenient access
__all__ = ["Settings", "get_settings", "BotMode", "LogLevel"]
