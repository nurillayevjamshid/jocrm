"""
Webhook mode bot setup
"""
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bot.config import get_settings
from bot.handlers import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


async def main() -> None:
    """Main bot entry point with webhook."""
    settings = get_settings()

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    dp.include_router(router)

    # Webhookni o'rnatish
    webhook_url = settings.WEBHOOK_URL
    if webhook_url:
        await bot.set_webhook(
            url=webhook_url,
            drop_pending_updates=True
        )
        logger.info(f"Webhook o'rnatildi: {webhook_url}")
    
    bot_info = await bot.get_me()
    logger.info(f"Bot started: @{bot_info.username} (ID: {bot_info.id})")
    logger.info(f"Mini App URL: {settings.MINIAPP_URL}")
    logger.info("Bot webhook mode da ishga tushdi!")

    # Webhook mode da polling ishlatilmaydi.
    # Bu yerda webhook o'rnatilgandan so'ng, bot Telegram dan kelayotgan
    # so'rovlarni kutishi kerak. Agar sizda webhook server bo'lsa,
    # u holda bu script faqat webhookni o'rnatish uchun xizmat qiladi.
    logger.info("Bot webhook rejimida sozlandi. Endi server so'rovlarni qabul qilishga tayyor.")
    
    # Webhook o'rnatilgandan keyin bot sessiyasini yopamiz
    await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
