"""Format output messages for BotBuilder."""

from typing import Dict, List
from services.parser import BotRequirements
from services.analyzer import BotArchitecture


def format_bot_overview(
    bot_name: str,
    requirements: BotRequirements,
    architecture: BotArchitecture
) -> str:
    """Format bot overview message."""
    lines = [
        f"🤖 **Bot Overview: {bot_name}**",
        "",
        f"**Purpose:** {requirements.purpose}",
        "",
    ]
    
    if requirements.features:
        lines.append("**Features:**")
        for feature in requirements.features:
            lines.append(f"  • {feature.title()}")
        lines.append("")
    
    if requirements.commands:
        lines.append("**Commands:**")
        for cmd in requirements.commands:
            lines.append(f"  • /{cmd}")
        lines.append("")
    
    if requirements.integrations:
        lines.append("**Integrations:**")
        for integration in requirements.integrations:
            lines.append(f"  • {integration.title()}")
        lines.append("")
    
    lines.append(f"**Language:** {requirements.language.title()}")
    
    return "\n".join(lines)


def format_deployment_status(bot_name: str, status: str, container_id: str = None) -> str:
    """Format deployment status message."""
    status_emoji = {
        "running": "✅",
        "stopped": "⏸️",
        "error": "❌",
        "building": "🔨",
    }.get(status, "❓")
    
    message = f"{status_emoji} **Bot: {bot_name}**\n"
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
        
        lines.append(f"{status_emoji} **{bot_name}** - {status.title()}")
    
    return "\n".join(lines)


def format_error_message(error: str) -> str:
    """Format error message."""
    return f"❌ **Error:** {error}\n\nPlease try again or contact support."


def format_success_message(message: str) -> str:
    """Format success message."""
    return f"✅ {message}"
