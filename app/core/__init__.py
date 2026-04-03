"""
Bot loader module.

Initializes aiogram bot, dispatcher, and related components.
Centralizes all bot-related object creation for clean dependency management.
"""

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.core.config import get_settings

# Load settings
settings = get_settings()

# Initialize bot with default properties
# Using DefaultBotProperties for cleaner configuration
bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
    )
)

# Initialize dispatcher
# Dispatcher is the main router for handling updates
dp = Dispatcher()

# Export bot and dispatcher for use in other modules
__all__ = ["bot", "dp", "settings"]
