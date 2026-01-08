"""Code generator for bot creation."""

from pathlib import Path
from typing import Dict
from jinja2 import Environment, FileSystemLoader, select_autoescape

from config import TEMPLATES_DIR, PYTHON_TEMPLATES_DIR, NODEJS_TEMPLATES_DIR, DOCKER_TEMPLATES_DIR
from services.parser import BotRequirements
from services.analyzer import BotArchitecture


class CodeGenerator:
    """Generate bot code from templates."""
    
    def __init__(self):
        self.env = Environment(
            loader=FileSystemLoader(str(TEMPLATES_DIR)),
            autoescape=select_autoescape(['html', 'xml'])
        )
    
    def generate_bot(
        self,
        bot_name: str,
        bot_token: str,
        requirements: BotRequirements,
        architecture: BotArchitecture
    ) -> Dict[str, str]:
        """Generate all bot files."""
        files = {}
        
        if requirements.language == "python":
            files.update(self._generate_python_bot(bot_name, bot_token, requirements, architecture))
        else:
            files.update(self._generate_nodejs_bot(bot_name, bot_token, requirements, architecture))
        
        # Generate Docker files
        files.update(self._generate_docker_files(bot_name, requirements, architecture))
        
        # Generate config files
        files.update(self._generate_config_files(bot_name, bot_token, requirements, architecture))
        
        return files
    
    def _generate_python_bot(
        self,
        bot_name: str,
        bot_token: str,
        requirements: BotRequirements,
        architecture: BotArchitecture
    ) -> Dict[str, str]:
        """Generate Python bot files."""
        files = {}
        
        context = {
            "bot_name": bot_name,
            "bot_token": bot_token,
            "requirements": requirements,
            "architecture": architecture,
            "commands": requirements.commands,
            "features": requirements.features,
        }
        
        # Main bot file
        template = self.env.get_template("python/main.py.j2")
        files["main.py"] = template.render(**context)
        
        # Handlers
        for handler in architecture.handlers:
            try:
                template = self.env.get_template(f"python/handlers/{handler}.py.j2")
                files[f"handlers/{handler}.py"] = template.render(**context)
            except Exception as e:
                # If template doesn't exist, create a basic handler
                handler_code = f'''"""{{handler}} command handler."""

from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("{handler}"))
async def handler(message: types.Message):
    """Handle /{handler} command."""
    await message.answer("Implement {handler} functionality here")
'''
                files[f"handlers/{handler}.py"] = handler_code
        
        # Services
        for service in architecture.services:
            try:
                template = self.env.get_template(f"python/services/{service}.py.j2")
                files[f"services/{service}.py"] = template.render(**context)
            except Exception as e:
                # If template doesn't exist, create a basic service
                service_code = f'''"""{{service}} service for {bot_name}."""

# Implement {service} service logic here
'''
                files[f"services/{service}.py"] = service_code
        
        # Requirements
        template = self.env.get_template("python/requirements.txt.j2")
        files["requirements.txt"] = template.render(**context)
        
        # Handlers __init__.py
        try:
            handlers_init = self.env.get_template("python/handlers/__init__.py.j2")
            files["handlers/__init__.py"] = handlers_init.render(**context)
        except Exception:
            # Fallback if template doesn't exist
            files["handlers/__init__.py"] = "# Handlers package\n"
        
        # Services __init__.py (if services exist)
        if architecture.services:
            try:
                services_init = self.env.get_template("python/services/__init__.py.j2")
                files["services/__init__.py"] = services_init.render(**context)
            except Exception:
                # Fallback if template doesn't exist
                files["services/__init__.py"] = "# Services package\n"
        
        return files
    
    def _generate_nodejs_bot(
        self,
        bot_name: str,
        bot_token: str,
        requirements: BotRequirements,
        architecture: BotArchitecture
    ) -> Dict[str, str]:
        """Generate Node.js bot files."""
        files = {}
        
        context = {
            "bot_name": bot_name,
            "bot_token": bot_token,
            "requirements": requirements,
            "architecture": architecture,
            "commands": requirements.commands,
            "features": requirements.features,
        }
        
        # Main bot file
        template = self.env.get_template("nodejs/index.js.j2")
        files["index.js"] = template.render(**context)
        
        # Handlers
        for handler in architecture.handlers:
            try:
                template = self.env.get_template(f"nodejs/handlers/{handler}.js.j2")
                files[f"handlers/{handler}.js"] = template.render(**context)
            except Exception as e:
                # If template doesn't exist, create a basic handler
                handler_code = f'''const {{ Telegraf }} = require('telegraf');

module.exports = (bot) => {{
    bot.command('{handler}', (ctx) => {{
        ctx.reply('Implement {handler} functionality here');
    }});
}};
'''
                files[f"handlers/{handler}.js"] = handler_code
        
        # Services
        for service in architecture.services:
            try:
                template = self.env.get_template(f"nodejs/services/{service}.js.j2")
                files[f"services/{service}.js"] = template.render(**context)
            except Exception as e:
                # If template doesn't exist, create a basic service
                service_code = f'''// {service} service for {bot_name}

// Implement {service} service logic here

module.exports = {{}};
'''
                files[f"services/{service}.js"] = service_code
        
        # Package.json
        template = self.env.get_template("nodejs/package.json.j2")
        files["package.json"] = template.render(**context)
        
        return files
    
    def _generate_docker_files(
        self,
        bot_name: str,
        requirements: BotRequirements,
        architecture: BotArchitecture
    ) -> Dict[str, str]:
        """Generate Docker files."""
        files = {}
        
        context = {
            "bot_name": bot_name,
            "language": requirements.language,
            "dependencies": architecture.dependencies,
        }
        
        if requirements.language == "python":
            template = self.env.get_template("docker/Dockerfile.python.j2")
            files["Dockerfile"] = template.render(**context)
        else:
            template = self.env.get_template("docker/Dockerfile.nodejs.j2")
            files["Dockerfile"] = template.render(**context)
        
        return files
    
    def _generate_config_files(
        self,
        bot_name: str,
        bot_token: str,
        requirements: BotRequirements,
        architecture: BotArchitecture
    ) -> Dict[str, str]:
        """Generate configuration files."""
        files = {}
        
        context = {
            "bot_name": bot_name,
            "config_vars": architecture.config_vars,
        }
        
        # .env.example
        template = self.env.get_template("env.example.j2")
        files[".env.example"] = template.render(**context)
        
        # .env (with actual token)
        env_content = f"BOT_TOKEN={bot_token}\n"
        for var in architecture.config_vars:
            if var != "BOT_TOKEN":
                env_content += f"{var}=\n"
        files[".env"] = env_content
        
        return files
