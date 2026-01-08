"""List bots command handler for BotBuilder."""

from aiogram import Router, types
from aiogram.filters import Command
from services.registry import BotRegistry
from utils.formatters import format_bot_list

router = Router()
registry = BotRegistry()


@router.message(Command("list"))
async def handler(message: types.Message):
    """Handle /list command."""
    user_id = message.from_user.id
    
    try:
        bots = await registry.get_user_bots(user_id)
        response = format_bot_list(bots)
        await message.answer(response, parse_mode="Markdown")
    except Exception as e:
        await message.answer(f"❌ Error listing bots: {str(e)}")
