"""
Bot handlers module.

Handles Telegram bot commands and interactions.
Main entry point to the Mini App CRM.
"""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from app.config import get_settings

router = Router()
settings = get_settings()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """
    Handle /start command.
    
    Sends welcome message with Web App button to open Mini App.
    This is the main entry point to the CRM system.
    """
    user = message.from_user
    
    # Build Web App button
    web_app_button = InlineKeyboardButton(
        text="🚀 CRM ni ochish",
        web_app=WebAppInfo(url=settings.MINIAPP_URL)
    )
    
    # Alternative button for browser users
    url_button = InlineKeyboardButton(
        text="🌐 Brauzerda ochish",
        url=settings.MINIAPP_URL
    )
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[web_app_button], [url_button]]
    )
    
    welcome_text = (
        f"<b>👋 Salom, {user.first_name}!</b>\n\n"
        f"Welcome to <b>For.Ever Cosmetics CRM</b>.\n\n"
        f"📱 <b>Asosiy xususiyatlar:</b>\n"
        f"• Mijozlar boshqaruvi\n"
        f"• Buyurtmalarni kuzatish\n"
        f"• Hisobotlar va statistika\n"
        f"• Real-time xabarnomalar\n\n"
        f"👇 <b>CRM tizimiga kirish uchun tugmani bosing:</b>"
    )
    
    await message.answer(welcome_text, reply_markup=keyboard)


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """Handle /help command."""
    help_text = (
        "<b>ℹ️ Yordam</b>\n\n"
        "<b>Asosiy buyruqlar:</b>\n"
        "/start - CRM tizimini ochish\n"
        "/help - Ushbu yordam xabari\n\n"
        "<b>Web App orqali:</b>\n"
        "• Mijozlar ro'yxatini ko'rish\n"
        "• Yangi buyurtma yaratish\n"
        "• Statistikani tahlil qilish\n\n"
        "<b>Qo'llab-quvvatlash:</b> @support"
    )
    await message.answer(help_text)


@router.message(F.text == "CRM")
async def text_crm(message: Message) -> None:
    """Handle 'CRM' text message."""
    await cmd_start(message)
