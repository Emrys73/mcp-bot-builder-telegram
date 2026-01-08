"""Help command handler for BotBuilder."""

from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("help"))
async def handler(message: types.Message):
    """Handle /help command."""
    help_text = """📖 **BotBuilder Help**

**Commands:**
• `/start` - Welcome message and introduction
• `/create` - Start creating a new bot
• `/list` - List all your deployed bots
• `/stop <bot_name>` - Stop a running bot
• `/start_bot <bot_name>` - Start a stopped bot
• `/status <bot_name>` - Check the status of a bot
• `/help` - Show this help message

**Creating a Bot:**
1. Use `/create` command
2. Describe your bot's functionality
3. Provide a unique bot name
4. Provide bot token from @BotFather
5. Wait for deployment (usually 1-2 minutes)
6. Start using your bot!

**Bot Features Supported:**
• Commands and handlers
• Database integration
• API integrations
• Payment processing
• File exports
• Reminders and scheduling
• And much more!

**Need Help?**
If you encounter any issues, make sure:
• Your bot token is valid (from @BotFather)
• Bot name is unique and doesn't contain special characters
• You haven't exceeded the bot limit per user

Happy bot building! 🎉
"""
    await message.answer(help_text, parse_mode="Markdown")
