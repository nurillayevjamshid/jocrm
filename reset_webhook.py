"""
Reset bot webhook and start polling
"""
import asyncio
from aiogram import Bot
from bot.config import get_settings

async def reset_and_start():
    settings = get_settings()
    bot = Bot(token=settings.BOT_TOKEN)
    
    # Webhookni o'chirish va pending updateslarni to'xtatish
    await bot.delete_webhook(drop_pending_updates=True)
    print("✅ Webhook o'chirildi, pending updates tozalandi")
    
    await bot.session.close()

if __name__ == "__main__":
    asyncio.run(reset_and_start())
