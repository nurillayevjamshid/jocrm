"""
Command handlers module.

Handles bot commands like /start, /help, etc.
Each command has its own handler function for clean separation of concerns.
"""

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

# Create a router for command handlers
# Router is used to group related handlers together
cmd_router = Router()


@cmd_router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """
    Handle /start command.
    
    This is the entry point for new users. Sends a welcome message
    with basic information about the bot.
    
    Args:
        message: The incoming message object from aiogram
    """
    user = message.from_user
    
    welcome_text = (
        f"<b>👋 Salom, {user.first_name}!</b>\n\n"
        f"Men <b>For.Ever Cosmetics</b> kompaniyasining CRM botiman.\n\n"
        f"📋 <b>Mavjud buyruqlar:</b>\n"
        f"/start - Botni ishga tushirish\n"
        f"/help - Yordam olish\n\n"
        f"🚀 Tez orada yangi imkoniyatlar qo'shiladi!"
    )
    
    await message.answer(welcome_text)


@cmd_router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """
    Handle /help command.
    
    Provides information about bot usage and available features.
    
    Args:
        message: The incoming message object from aiogram
    """
    help_text = (
        "<b>ℹ️ Yordam</b>\n\n"
        "Bu bot orqali siz:\n"
        "• Mijozlar ma'lumotlarini boshqarishingiz\n"
        "• Buyurtmalarni kuzatishingiz\n"
        "• Hisobotlarni olishingiz mumkin\n\n"
        "<b>Bog'lanish:</b> @admin_username"
    )
    
    await message.answer(help_text)
