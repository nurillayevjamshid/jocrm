"""
Handlers initialization module.

Registers all routers with the main dispatcher.
This is the central point for handler registration.
"""

from app.core import dp
from app.handlers.commands import cmd_router
from app.handlers.messages import msg_router


def register_handlers() -> None:
    """
    Register all handler routers with the dispatcher.
    
    Routers are registered in order of priority - command handlers
    should be registered before general message handlers to ensure
    commands are processed first.
    
    The order matters: first registered = first checked
    """
    # Register command handlers first (higher priority)
    dp.include_router(cmd_router)
    
    # Register message handlers (lower priority, catch-all)
    dp.include_router(msg_router)


def setup_handlers() -> None:
    """
    Setup all handlers. Called during application startup.
    """
    register_handlers()
