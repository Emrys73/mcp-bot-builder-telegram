"""Status command handler for BotBuilder."""

from aiogram import Router, types
from aiogram.filters import Command
from services.registry import BotRegistry
from services.deployment import DeploymentService
from utils.formatters import format_deployment_status, format_error_message

router = Router()
registry = BotRegistry()
deployment = DeploymentService()


@router.message(Command("status"))
async def handler(message: types.Message):
    """Handle /status command."""
    user_id = message.from_user.id
    args = message.text.split()[1:] if message.text else []
    
    if not args:
        await message.answer("❌ Please provide a bot name: `/status <bot_name>`", parse_mode="Markdown")
        return
    
    bot_name = args[0]
    
    try:
        # Get bot metadata
        bot = await registry.get_bot(user_id, bot_name)
        if not bot:
            await message.answer(f"❌ Bot '{bot_name}' not found.")
            return
        
        container_id = bot.get("container_id")
        status = bot.get("status", "unknown")
        
        # Get actual container status
        if container_id:
            actual_status = deployment.get_container_status(container_id)
            if actual_status:
                status = actual_status
                # Update registry if status changed
                if actual_status != bot.get("status"):
                    await registry.update_bot_status(user_id, bot_name, actual_status)
        
        response = format_deployment_status(bot_name, status, container_id)
        await message.answer(response, parse_mode="Markdown")
    except Exception as e:
        await message.answer(format_error_message(str(e)))
