"""Start command handler for BotBuilder."""

from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def handler(message: types.Message):
    """Handle /start command."""
    welcome_text = """👋 **Welcome to BotBuilder!**

I'm an expert Telegram Bot Architect. I can create and deploy complete Telegram bots for you automatically.

**How it works:**
1. Describe the bot you want to create
2. Provide a bot name and token (from @BotFather)
3. I'll generate, deploy, and start your bot on my server
4. You can interact with your bot immediately!

**Commands:**
• `/create` - Create a new bot
• `/list` - List your deployed bots
• `/stop <bot_name>` - Stop a bot
• `/start_bot <bot_name>` - Start a stopped bot
• `/status <bot_name>` - Check bot status
• `/help` - Show this help message

**Example:**
Send: `/create`
Then describe: "I want an expense tracker bot with categories"

Ready to create your first bot? Use `/create` to get started! 🚀
"""
    await message.answer(welcome_text, parse_mode="Markdown")
