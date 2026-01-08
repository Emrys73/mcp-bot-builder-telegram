"""Parse user requirements from natural language descriptions."""

import re
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class BotRequirements:
    """Structured bot requirements."""
    purpose: str
    features: List[str]
    commands: List[str]
    integrations: List[str]
    language: str  # "python" or "nodejs"
    needs_database: bool
    needs_payments: bool
    needs_api: bool


class RequirementParser:
    """Parse natural language bot descriptions into structured requirements."""
    
    # Common feature keywords
    FEATURE_KEYWORDS = {
        "database": ["database", "db", "sqlite", "postgres", "mysql", "store data", "save data"],
        "payments": ["payment", "pay", "stripe", "paypal", "money", "transaction"],
        "api": ["api", "external", "fetch", "http", "request", "weather", "news"],
        "categories": ["category", "categories", "group", "tag"],
        "export": ["export", "csv", "excel", "download", "file"],
        "reminder": ["reminder", "notify", "alert", "schedule"],
        "search": ["search", "find", "query", "filter"],
    }
    
    # Command patterns
    COMMAND_PATTERNS = [
        r"/\w+",  # /command
        r"command\s+(\w+)",  # command add
        r"(\w+)\s+command",  # add command
    ]
    
    def parse(self, description: str) -> BotRequirements:
        """Parse bot description into structured requirements."""
        description_lower = description.lower()
        
        # Extract purpose (first sentence or main description)
        purpose = self._extract_purpose(description)
        
        # Extract features
        features = self._extract_features(description_lower)
        
        # Extract commands
        commands = self._extract_commands(description)
        
        # Detect integrations
        needs_database = self._has_feature(description_lower, "database")
        needs_payments = self._has_feature(description_lower, "payments")
        needs_api = self._has_feature(description_lower, "api")
        
        integrations = []
        if needs_database:
            integrations.append("database")
        if needs_payments:
            integrations.append("payments")
        if needs_api:
            integrations.append("api")
        
        # Detect language preference (default to Python)
        language = self._detect_language(description_lower)
        
        return BotRequirements(
            purpose=purpose,
            features=features,
            commands=commands,
            integrations=integrations,
            language=language,
            needs_database=needs_database,
            needs_payments=needs_payments,
            needs_api=needs_api
        )
    
    def _extract_purpose(self, description: str) -> str:
        """Extract bot purpose from description."""
        # Take first sentence or first 200 characters
        sentences = re.split(r'[.!?]\s+', description)
        if sentences:
            purpose = sentences[0].strip()
            if len(purpose) > 200:
                purpose = purpose[:200] + "..."
            return purpose
        return description[:200] if len(description) > 200 else description
    
    def _extract_features(self, description_lower: str) -> List[str]:
        """Extract features from description."""
        features = []
        
        for feature, keywords in self.FEATURE_KEYWORDS.items():
            if any(keyword in description_lower for keyword in keywords):
                features.append(feature)
        
        # Add common features based on context
        if "track" in description_lower or "log" in description_lower:
            features.append("tracking")
        if "list" in description_lower or "show" in description_lower:
            features.append("listing")
        if "add" in description_lower or "create" in description_lower:
            features.append("creation")
        if "delete" in description_lower or "remove" in description_lower:
            features.append("deletion")
        
        return list(set(features))  # Remove duplicates
    
    def _extract_commands(self, description: str) -> List[str]:
        """Extract commands from description."""
        commands = []
        
        # Find explicit command mentions
        for pattern in self.COMMAND_PATTERNS:
            matches = re.findall(pattern, description, re.IGNORECASE)
            commands.extend(matches)
        
        # Infer common commands from features
        description_lower = description.lower()
        if "add" in description_lower or "create" in description_lower:
            commands.append("/add")
        if "list" in description_lower or "show" in description_lower:
            commands.append("/list")
        if "delete" in description_lower or "remove" in description_lower:
            commands.append("/delete")
        if "start" in description_lower:
            commands.append("/start")
        if "help" in description_lower:
            commands.append("/help")
        
        # Clean and deduplicate
        commands = [cmd.strip('/') if cmd.startswith('/') else cmd for cmd in commands]
        commands = list(set(commands))
        
        return commands[:10]  # Limit to 10 commands
    
    def _has_feature(self, description_lower: str, feature: str) -> bool:
        """Check if description mentions a specific feature."""
        keywords = self.FEATURE_KEYWORDS.get(feature, [])
        return any(keyword in description_lower for keyword in keywords)
    
    def _detect_language(self, description_lower: str) -> str:
        """Detect preferred language (default: python)."""
        if any(word in description_lower for word in ["node", "nodejs", "javascript", "js", "telegraf"]):
            return "nodejs"
        return "python"  # Default to Python
