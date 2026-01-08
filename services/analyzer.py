"""Analyze requirements and design bot architecture."""

from typing import Dict, List
from dataclasses import dataclass

from services.parser import BotRequirements


@dataclass
class BotArchitecture:
    """Designed bot architecture."""
    handlers: List[str]
    services: List[str]
    middleware: List[str]
    dependencies: List[str]
    file_structure: Dict[str, List[str]]
    config_vars: List[str]


class ArchitectureAnalyzer:
    """Analyze requirements and design bot architecture."""
    
    def analyze(self, requirements: BotRequirements) -> BotArchitecture:
        """Design bot architecture based on requirements."""
        handlers = self._design_handlers(requirements)
        services = self._design_services(requirements)
        middleware = self._design_middleware(requirements)
        dependencies = self._design_dependencies(requirements)
        file_structure = self._design_file_structure(requirements, handlers, services)
        config_vars = self._design_config_vars(requirements)
        
        return BotArchitecture(
            handlers=handlers,
            services=services,
            middleware=middleware,
            dependencies=dependencies,
            file_structure=file_structure,
            config_vars=config_vars
        )
    
    def _design_handlers(self, req: BotRequirements) -> List[str]:
        """Design handler structure."""
        handlers = ["start", "help"]  # Always include
        
        # Add handlers based on commands
        command_handlers = {
            "add": "add",
            "create": "add",
            "list": "list",
            "show": "list",
            "delete": "delete",
            "remove": "delete",
            "update": "update",
            "edit": "update",
            "search": "search",
            "find": "search",
        }
        
        for cmd in req.commands:
            cmd_lower = cmd.lower().strip('/')
            if cmd_lower in command_handlers:
                handler = command_handlers[cmd_lower]
                if handler not in handlers:
                    handlers.append(handler)
        
        # Add feature-specific handlers
        if "tracking" in req.features:
            handlers.append("track")
        if "reminder" in req.features:
            handlers.append("reminder")
        if "export" in req.features:
            handlers.append("export")
        
        return list(set(handlers))
    
    def _design_services(self, req: BotRequirements) -> List[str]:
        """Design service structure."""
        services = []
        
        if req.needs_database:
            services.append("database")
        if req.needs_payments:
            services.append("payment")
        if req.needs_api:
            services.append("api_client")
        if "export" in req.features:
            services.append("exporter")
        if "reminder" in req.features:
            services.append("scheduler")
        
        return services
    
    def _design_middleware(self, req: BotRequirements) -> List[str]:
        """Design middleware structure."""
        middleware = ["logging", "error_handler"]
        
        if req.needs_database:
            middleware.append("db_session")
        
        return middleware
    
    def _design_dependencies(self, req: BotRequirements) -> List[str]:
        """Design dependency list."""
        deps = []
        
        if req.language == "python":
            deps.extend(["aiogram>=3.0.0", "python-dotenv>=1.0.0"])
            if req.needs_database:
                deps.append("aiosqlite>=0.19.0")
            if req.needs_api:
                deps.append("aiohttp>=3.9.0")
            if "export" in req.features:
                deps.append("pandas>=2.0.0")
        else:  # nodejs
            deps.extend(["telegraf", "dotenv"])
            if req.needs_database:
                deps.append("better-sqlite3")
            if req.needs_api:
                deps.append("axios")
            if "export" in req.features:
                deps.append("csv-writer")
        
        return deps
    
    def _design_file_structure(
        self,
        req: BotRequirements,
        handlers: List[str],
        services: List[str]
    ) -> Dict[str, List[str]]:
        """Design file structure."""
        structure = {
            "root": ["main.py" if req.language == "python" else "index.js", "config.py" if req.language == "python" else "config.js"],
            "handlers": [f"{h}.py" if req.language == "python" else f"{h}.js" for h in handlers],
            "services": [f"{s}.py" if req.language == "python" else f"{s}.js" for s in services] if services else [],
        }
        
        if req.needs_database:
            structure["root"].append("database.py" if req.language == "python" else "database.js")
        
        return structure
    
    def _design_config_vars(self, req: BotRequirements) -> List[str]:
        """Design configuration variables."""
        vars = ["BOT_TOKEN"]
        
        if req.needs_database:
            vars.append("DATABASE_URL")
        if req.needs_payments:
            vars.extend(["PAYMENT_PROVIDER", "PAYMENT_API_KEY"])
        if req.needs_api:
            vars.append("API_KEY")
        
        return vars
