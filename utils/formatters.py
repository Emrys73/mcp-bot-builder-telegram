"""Format output messages for BotBuilder."""

from typing import Dict, List
from services.parser import BotRequirements
from services.analyzer import BotArchitecture


def escape_markdown(text: str) -> str:
    """Escape Markdown special characters to prevent parsing errors."""
    if not text:
        return ""
    # Escape Markdown special characters
    escape_chars = ['*', '_', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in escape_chars:
        text = text.replace(char, f'\\{char}')
    return text


def format_bot_overview(
    bot_name: str,
    requirements: BotRequirements,
    architecture: BotArchitecture
) -> str:
    """Format bot overview message."""
    # Escape user-provided content to prevent Markdown parsing errors
    safe_bot_name = escape_markdown(bot_name)
    safe_purpose = escape_markdown(requirements.purpose)
    
    lines = [
        f"🤖 **Bot Overview: {safe_bot_name}**",
        "",
        f"**Purpose:** {safe_purpose}",
        "",
    ]
    
    if requirements.features:
        lines.append("**Features:**")
        for feature in requirements.features:
            safe_feature = escape_markdown(feature.title())
            lines.append(f"  • {safe_feature}")
        lines.append("")
    
    if requirements.commands:
        lines.append("**Commands:**")
        for cmd in requirements.commands:
            safe_cmd = escape_markdown(cmd)
            lines.append(f"  • /{safe_cmd}")
        lines.append("")
    
    if requirements.integrations:
        lines.append("**Integrations:**")
        for integration in requirements.integrations:
            safe_integration = escape_markdown(integration.title())
            lines.append(f"  • {safe_integration}")
        lines.append("")
    
    safe_language = escape_markdown(requirements.language.title())
    lines.append(f"**Language:** {safe_language}")
    
    return "\n".join(lines)


def format_deployment_status(bot_name: str, status: str, container_id: str = None) -> str:
    """Format deployment status message."""
    status_emoji = {
        "running": "✅",
        "stopped": "⏸️",
        "error": "❌",
        "building": "🔨",
    }.get(status, "❓")
    
    safe_bot_name = escape_markdown(bot_name)
    message = f"{status_emoji} **Bot: {safe_bot_name}**\n"
    message += f"Status: {status.title()}\n"
    
    if container_id:
        message += f"Container ID: `{container_id[:12]}`"
    
    return message


def format_bot_list(bots: Dict[str, Dict]) -> str:
    """Format list of user's bots."""
    if not bots:
        return "📭 You don't have any deployed bots yet.\n\nUse /create to create your first bot!"
    
    lines = ["🤖 **Your Bots:**", ""]
    
    for bot_name, bot_info in bots.items():
        status = bot_info.get("status", "unknown")
        status_emoji = {
            "running": "🟢",
            "stopped": "🔴",
            "error": "🔴",
        }.get(status, "⚪")
        
        safe_bot_name = escape_markdown(bot_name)
        lines.append(f"{status_emoji} **{safe_bot_name}** - {status.title()}")
    
    return "\n".join(lines)


def format_error_message(error: str) -> str:
    """Format error message."""
    safe_error = escape_markdown(str(error))
    return f"❌ **Error:** {safe_error}\n\nPlease try again or contact support."


def format_success_message(message: str) -> str:
    """Format success message."""
    return f"✅ {message}"
