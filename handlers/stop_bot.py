"""Stop bot command handler for BotBuilder."""

from aiogram import Router, types
from aiogram.filters import Command
from services.registry import BotRegistry
from services.deployment import DeploymentService
from utils.formatters import format_success_message, format_error_message

router = Router()
registry = BotRegistry()
deployment = DeploymentService()


@router.message(Command("stop"))
async def handler(message: types.Message):
    """Handle /stop command."""
    user_id = message.from_user.id
    args = message.text.split()[1:] if message.text else []
    
    if not args:
        await message.answer("❌ Please provide a bot name: `/stop <bot_name>`", parse_mode="Markdown")
        return
    
    bot_name = args[0]
    
    try:
        # Get bot metadata
        bot = await registry.get_bot(user_id, bot_name)
        if not bot:
            await message.answer(f"❌ Bot '{bot_name}' not found.")
            return
        
        container_id = bot.get("container_id")
        if not container_id:
            await message.answer(f"❌ No container found for bot '{bot_name}'.")
            return
        
        # Stop container
        success = deployment.stop_container(container_id)
        if success:
            await registry.update_bot_status(user_id, bot_name, "stopped")
            await message.answer(format_success_message(f"Bot '{bot_name}' stopped successfully."))
        else:
            await message.answer(format_error_message(f"Failed to stop bot '{bot_name}'."))
    except Exception as e:
        await message.answer(format_error_message(str(e)))
