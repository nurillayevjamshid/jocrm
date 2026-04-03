"""
Main Entry Point - For.Ever Cosmetics CRM

Usage:
    python main.py           # Run bot (default)
    python main.py --api     # Run backend API
"""

import argparse
import asyncio
import logging
import sys

from bot.main import main as bot_main
from backend.main import app as api_app

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def run_bot():
    """Run Telegram bot."""
    try:
        asyncio.run(bot_main())
    except KeyboardInterrupt:
        logger.info("Stopped by user")
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)


def run_api():
    """Run FastAPI backend."""
    import uvicorn
    from backend.config import get_settings
    settings = get_settings()
    uvicorn.run(
        "backend.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="For.Ever Cosmetics CRM")
    parser.add_argument("--api", action="store_true", help="Run backend API instead of bot")
    args = parser.parse_args()

    if args.api:
        run_api()
    else:
        run_bot()
