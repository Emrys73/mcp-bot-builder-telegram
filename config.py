"""Configuration management for BotBuilder."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# BotBuilder bot token (required)
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is required")

# Directory for deployed bots
BOTS_DIR = Path(os.getenv("BOTS_DIR", "./bots"))
BOTS_DIR.mkdir(exist_ok=True)

# Docker configuration
DOCKER_NETWORK = os.getenv("DOCKER_NETWORK", "botbuilder_network")

# Bot limits
MAX_BOTS_PER_USER = int(os.getenv("MAX_BOTS_PER_USER", "10"))

# Template paths
TEMPLATES_DIR = Path(__file__).parent / "templates"
PYTHON_TEMPLATES_DIR = TEMPLATES_DIR / "python"
NODEJS_TEMPLATES_DIR = TEMPLATES_DIR / "nodejs"
DOCKER_TEMPLATES_DIR = TEMPLATES_DIR / "docker"

# Registry file path
REGISTRY_FILE = Path(__file__).parent / "bot_registry.json"
