# BotBuilder - Expert Telegram Bot Architect

BotBuilder is an intelligent Telegram bot that automatically generates, deploys, and manages Telegram bots on your server. Users describe their desired bot functionality, and BotBuilder creates a complete, production-ready bot deployed in a Docker container.

## Features

- 🤖 **Automatic Bot Generation**: Create complete Telegram bots from natural language descriptions
- 🐳 **Docker Deployment**: Each bot runs in its own isolated Docker container
- 📝 **Smart Code Generation**: Generates production-ready code with proper structure
- 🔧 **Bot Management**: List, start, stop, and monitor your deployed bots
- 🎯 **Multiple Frameworks**: Supports Python (aiogram) and Node.js (telegraf)
- 🔒 **Secure**: Environment variables for tokens, isolated containers

## Architecture

```
BotBuilder Bot (Main Process)
    ↓
User Request → Parse Requirements → Design Architecture → Generate Code
    ↓
Create Files → Build Docker Image → Create Container → Start Bot
    ↓
Bot Running on Server (Docker Container)
```

## Prerequisites

- Python 3.13+
- Docker installed and running
- Docker daemon accessible
- Telegram bot token for BotBuilder (from @BotFather)

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd mcp-telegram-bot
```

2. **Create virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment:**
```bash
cp .env.example .env
# Edit .env and add your BOT_TOKEN
```

5. **Ensure Docker is running:**
```bash
docker --version
docker ps  # Should work without errors
```

## Usage

1. **Start BotBuilder:**
```bash
python main.py
```

2. **Interact with BotBuilder on Telegram:**
   - Find your bot on Telegram
   - Send `/start` to begin
   - Use `/create` to create a new bot
   - Follow the prompts to describe your bot

3. **Example Bot Creation:**
```
User: /create
BotBuilder: Describe your bot...
User: I want an expense tracker bot with categories and CSV export
BotBuilder: What's the bot name?
User: expense_tracker
BotBuilder: Provide bot token from @BotFather
User: 123456:ABC-DEF...
BotBuilder: ✅ Bot deployed successfully!
```

## Commands

- `/start` - Welcome message and introduction
- `/create` - Create a new bot
- `/list` - List all your deployed bots
- `/stop <bot_name>` - Stop a running bot
- `/start_bot <bot_name>` - Start a stopped bot
- `/status <bot_name>` - Check bot status
- `/help` - Show help message

## Project Structure

```
mcp-telegram-bot/
├── main.py                 # BotBuilder entry point
├── config.py              # Configuration
├── handlers/              # BotBuilder handlers
│   ├── start.py
│   ├── create_bot.py
│   ├── list_bots.py
│   └── ...
├── services/              # Core services
│   ├── parser.py          # Parse requirements
│   ├── analyzer.py        # Design architecture
│   ├── generator.py       # Generate code
│   ├── file_manager.py    # File operations
│   ├── deployment.py      # Docker operations
│   └── registry.py         # Bot registry
├── templates/             # Code templates
│   ├── python/
│   ├── nodejs/
│   └── docker/
├── bots/                  # Deployed bots (created at runtime)
└── requirements.txt
```

## Environment Variables

- `BOT_TOKEN` - Telegram bot token for BotBuilder (required)
- `BOTS_DIR` - Directory for deployed bots (default: `./bots`)
- `DOCKER_NETWORK` - Docker network name (default: `botbuilder_network`)
- `MAX_BOTS_PER_USER` - Maximum bots per user (default: `10`)

## Generated Bot Structure

Each generated bot includes:
- Main bot file (`main.py` or `index.js`)
- Handlers directory with command handlers
- Services directory (if needed)
- Configuration files
- Dockerfile
- Requirements/package.json
- Environment files

## Docker Integration

- Each bot runs in its own Docker container
- Containers are isolated and managed independently
- Automatic restart policy (unless-stopped)
- Network isolation via Docker network

## Limitations

- Maximum bots per user: 10 (configurable)
- Bot names must be unique per user
- Requires Docker to be running
- Server must have sufficient resources

## Troubleshooting

**Docker connection error:**
- Ensure Docker daemon is running: `docker ps`
- Check Docker socket permissions

**Bot creation fails:**
- Verify bot token is valid
- Check Docker logs: `docker logs <container_id>`
- Ensure sufficient disk space

**Container won't start:**
- Check container logs: `docker logs botbuilder-<bot_name>`
- Verify environment variables are set correctly

## Development

To contribute or modify BotBuilder:

1. Install development dependencies
2. Modify templates in `templates/` directory
3. Update services as needed
4. Test with a test bot token

## License

[Add your license here]

## Support

For issues or questions, please open an issue on the repository.
