"""Create bot command handler for BotBuilder."""

from aiogram import Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services.parser import RequirementParser
from services.analyzer import ArchitectureAnalyzer
from services.generator import CodeGenerator
from services.file_manager import FileManager
from services.deployment import DeploymentService
from services.registry import BotRegistry
from utils.formatters import format_bot_overview, format_success_message, format_error_message
from config import MAX_BOTS_PER_USER

router = Router()

# Initialize services
parser = RequirementParser()
analyzer = ArchitectureAnalyzer()
generator = CodeGenerator()
file_manager = FileManager()
deployment = DeploymentService()
registry = BotRegistry()


class BotCreationStates(StatesGroup):
    """FSM states for bot creation."""
    waiting_description = State()
    waiting_name = State()
    waiting_token = State()


@router.message(Command("create"))
async def create_command(message: types.Message, state: FSMContext):
    """Start bot creation process."""
    user_id = message.from_user.id
    
    # Check bot limit
    bot_count = await registry.count_user_bots(user_id)
    if bot_count >= MAX_BOTS_PER_USER:
        await message.answer(
            f"❌ You've reached the maximum limit of {MAX_BOTS_PER_USER} bots per user."
        )
        return
    
    await message.answer(
        "🤖 **Let's create your bot!**\n\n"
        "Please describe what you want your bot to do.\n\n"
        "Example: \"I want an expense tracker bot with categories and CSV export\"",
        parse_mode="Markdown"
    )
    await state.set_state(BotCreationStates.waiting_description)


@router.message(StateFilter(BotCreationStates.waiting_description))
async def process_description(message: types.Message, state: FSMContext):
    """Process bot description."""
    description = message.text
    
    if not description or len(description) < 10:
        await message.answer("❌ Please provide a more detailed description (at least 10 characters).")
        return
    
    await state.update_data(description=description)
    await message.answer(
        "✅ Description received!\n\n"
        "Now, please provide a **unique name** for your bot.\n\n"
        "The name should:\n"
        "• Be lowercase with underscores (e.g., `expense_tracker`)\n"
        "• Not contain spaces or special characters\n"
        "• Be unique (not already used)",
        parse_mode="Markdown"
    )
    await state.set_state(BotCreationStates.waiting_name)


@router.message(StateFilter(BotCreationStates.waiting_name))
async def process_name(message: types.Message, state: FSMContext):
    """Process bot name."""
    bot_name = message.text.strip().lower()
    
    # Validate name
    if not bot_name.replace('_', '').replace('-', '').isalnum():
        await message.answer(
            "❌ Invalid bot name. Use only lowercase letters, numbers, underscores, and hyphens."
        )
        return
    
    user_id = message.from_user.id
    
    # Check if name already exists
    existing_bot = await registry.get_bot(user_id, bot_name)
    if existing_bot:
        await message.answer(f"❌ Bot name '{bot_name}' is already taken. Please choose another name.")
        return
    
    # Check if directory exists
    if file_manager.bot_exists(bot_name):
        await message.answer(f"❌ Bot name '{bot_name}' conflicts with existing bot. Please choose another name.")
        return
    
    await state.update_data(bot_name=bot_name)
    await message.answer(
        "✅ Bot name accepted!\n\n"
        "Now, please provide your **bot token** from @BotFather.\n\n"
        "To get a token:\n"
        "1. Open @BotFather on Telegram\n"
        "2. Send `/newbot` command\n"
        "3. Follow the instructions\n"
        "4. Copy the token and send it here\n\n"
        "The token looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`",
        parse_mode="Markdown"
    )
    await state.set_state(BotCreationStates.waiting_token)


@router.message(StateFilter(BotCreationStates.waiting_token))
async def process_token(message: types.Message, state: FSMContext):
    """Process bot token and create bot."""
    bot_token = message.text.strip()
    
    # Basic token validation (format: numbers:letters)
    if ':' not in bot_token or len(bot_token) < 20:
        await message.answer(
            "❌ Invalid bot token format. Please provide a valid token from @BotFather."
        )
        return
    
    user_id = message.from_user.id
    data = await state.get_data()
    description = data.get("description")
    bot_name = data.get("bot_name")
    
    # Show processing message
    processing_msg = await message.answer("🔄 Processing your request... This may take a minute.")
    
    try:
        # Parse requirements
        requirements = parser.parse(description)
        
        # Analyze architecture
        architecture = analyzer.analyze(requirements)
        
        # Generate code
        await processing_msg.edit_text("📝 Generating bot code...")
        files = generator.generate_bot(bot_name, bot_token, requirements, architecture)
        
        # Create directory and write files
        await processing_msg.edit_text("💾 Writing files...")
        bot_dir = await file_manager.create_bot_directory(bot_name)
        await file_manager.write_files(bot_name, files)
        
        # Build Docker image
        await processing_msg.edit_text("🐳 Building Docker image...")
        image_tag = deployment.build_image(bot_name, bot_dir)
        if not image_tag:
            raise Exception("Failed to build Docker image")
        
        # Create container
        await processing_msg.edit_text("📦 Creating container...")
        container_id = deployment.create_container(bot_name, image_tag, bot_token)
        if not container_id:
            raise Exception("Failed to create Docker container")
        
        # Start container
        await processing_msg.edit_text("🚀 Starting bot...")
        started = deployment.start_container(container_id)
        if not started:
            raise Exception("Failed to start container")
        
        # Register bot
        await registry.register_bot(user_id, bot_name, bot_token, container_id, "running")
        
        # Success message
        overview = format_bot_overview(bot_name, requirements, architecture)
        success_msg = (
            f"{overview}\n\n"
            f"✅ **Bot deployed successfully!**\n\n"
            f"Your bot is now running. You can interact with it using the token you provided.\n\n"
            f"**Bot Name:** `{bot_name}`\n"
            f"**Status:** Running\n"
            f"**Container ID:** `{container_id[:12]}`\n\n"
            f"Use `/list` to see all your bots or `/status {bot_name}` to check status."
        )
        
        await processing_msg.edit_text(success_msg, parse_mode="Markdown")
        await state.clear()
        
    except Exception as e:
        error_msg = format_error_message(f"Failed to create bot: {str(e)}")
        await processing_msg.edit_text(error_msg, parse_mode="Markdown")
        await state.clear()
