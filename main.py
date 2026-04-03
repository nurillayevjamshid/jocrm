"""
Main application entry point.

Initializes and runs the Telegram bot with polling.
Handles graceful shutdown on exit signals.
"""

import asyncio
import logging
import signal
import sys

from app.core import bot, dp
from app.handlers import setup_handlers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


async def on_startup() -> None:
    """
    Actions to perform on bot startup.
    
    - Register all handlers
    - Log startup information
    - Initialize any required services
    """
    logger.info("Starting bot...")
    
    # Setup handlers
    setup_handlers()
    logger.info("Handlers registered successfully")
    
    # Log bot info
    bot_info = await bot.get_me()
    logger.info(f"Bot started: @{bot_info.username} (ID: {bot_info.id})")


async def on_shutdown() -> None:
    """
    Actions to perform on bot shutdown.
    
    - Close bot session
    - Cleanup resources
    - Log shutdown
    """
    logger.info("Shutting down bot...")
    
    # Close bot session
    await bot.session.close()
    logger.info("Bot session closed")
    
    logger.info("Bot stopped successfully")


async def main() -> None:
    """
    Main function to run the bot.
    
    Uses polling mode for development. For production with webhook,
    this would be replaced with webhook configuration.
    """
    # Run startup sequence
    await on_startup()
    
    try:
        # Start polling
        # drop_pending_updates=True - skip updates that arrived while bot was offline
        # on_shutdown - cleanup function called on exit
        logger.info("Starting polling...")
        await dp.start_polling(
            bot,
            skip_updates=True,
            on_shutdown=on_shutdown
        )
    except Exception as e:
        logger.error(f"Error during polling: {e}")
        raise


if __name__ == "__main__":
    try:
        # Run the main async function
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (KeyboardInterrupt)")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
