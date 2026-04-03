"""
Message handlers module.

Handles text messages and other non-command user inputs.
All non-command text processing logic belongs here.
"""

from aiogram import Router
from aiogram.types import Message

# Create a router for message handlers
msg_router = Router()


@msg_router.message()
async def handle_text_message(message: Message) -> None:
    """
    Handle incoming text messages.
    
    This is the default handler for text messages that don't match
    any command. Currently echoes back the message with additional info.
    
    Args:
        message: The incoming message object from aiogram
    """
    # Check if message has text content
    if not message.text:
        return
    
    user = message.from_user
    
    # Echo response with user info
    response_text = (
        f"<b>📨 Xabar qabul qilindi!</b>\n\n"
        f"<b>Sizning xabaringiz:</b>\n"
        f"<i>{message.text}</i>\n\n"
        f"👤 <b>Foydalanuvchi:</b> {user.first_name}\n"
        f"🆔 <b>ID:</b> <code>{user.id}</code>\n\n"
        f"<i>⚡️ Tez orada to'liq funksionallik qo'shiladi...</i>"
    )
    
    await message.answer(response_text)
