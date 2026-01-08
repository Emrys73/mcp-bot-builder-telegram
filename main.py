"""Main entry point for BotBuilder bot."""

import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from handlers import start, help, create_bot, list_bots, stop_bot, start_bot, status

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    """Main bot function."""
    logger.info("Starting BotBuilder bot...")
    
    # Initialize bot and dispatcher
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN)
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Register handlers
    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(create_bot.router)
    dp.include_router(list_bots.router)
    dp.include_router(stop_bot.router)
    dp.include_router(start_bot.router)
    dp.include_router(status.router)
    
    logger.info("BotBuilder bot is running...")
    
    # Start polling
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error in bot: {e}", exc_info=True)
    finally:
        await bot.session.close()
        logger.info("BotBuilder bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())
