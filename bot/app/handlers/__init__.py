"""
Bot handlers initialization.
"""

from aiogram import Dispatcher
from app.handlers.commands import router as commands_router


def setup_handlers(dp: Dispatcher) -> None:
    """Register all handlers with dispatcher."""
    dp.include_router(commands_router)
