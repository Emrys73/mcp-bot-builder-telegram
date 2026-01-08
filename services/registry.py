"""Bot registry for managing deployed bots metadata."""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import aiofiles

from config import REGISTRY_FILE


class BotRegistry:
    """Manages bot metadata and lifecycle."""
    
    def __init__(self):
        self.registry_file = REGISTRY_FILE
        self._ensure_registry_exists()
    
    def _ensure_registry_exists(self):
        """Create registry file if it doesn't exist."""
        if not self.registry_file.exists():
            self.registry_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.registry_file, 'w') as f:
                json.dump({}, f)
    
    async def _load_registry(self) -> Dict:
        """Load registry from file."""
        async with aiofiles.open(self.registry_file, 'r') as f:
            content = await f.read()
            return json.loads(content) if content else {}
    
    async def _save_registry(self, registry: Dict):
        """Save registry to file."""
        async with aiofiles.open(self.registry_file, 'w') as f:
            await f.write(json.dumps(registry, indent=2))
    
    async def register_bot(
        self,
        user_id: int,
        bot_name: str,
        bot_token: str,
        container_id: Optional[str] = None,
        status: str = "running"
    ) -> bool:
        """Register a new bot."""
        registry = await self._load_registry()
        
        # Initialize user entry if not exists
        if str(user_id) not in registry:
            registry[str(user_id)] = {}
        
        # Check if bot name already exists for this user
        if bot_name in registry[str(user_id)]:
            return False
        
        # Register bot
        registry[str(user_id)][bot_name] = {
            "bot_token": bot_token,
            "container_id": container_id,
            "status": status,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        await self._save_registry(registry)
        return True
    
    async def get_user_bots(self, user_id: int) -> Dict[str, Dict]:
        """Get all bots for a user."""
        registry = await self._load_registry()
        return registry.get(str(user_id), {})
    
    async def get_bot(self, user_id: int, bot_name: str) -> Optional[Dict]:
        """Get specific bot metadata."""
        bots = await self.get_user_bots(user_id)
        return bots.get(bot_name)
    
    async def update_bot_status(
        self,
        user_id: int,
        bot_name: str,
        status: str,
        container_id: Optional[str] = None
    ) -> bool:
        """Update bot status."""
        registry = await self._load_registry()
        
        if str(user_id) not in registry or bot_name not in registry[str(user_id)]:
            return False
        
        bot = registry[str(user_id)][bot_name]
        bot["status"] = status
        bot["updated_at"] = datetime.now().isoformat()
        
        if container_id is not None:
            bot["container_id"] = container_id
        
        await self._save_registry(registry)
        return True
    
    async def delete_bot(self, user_id: int, bot_name: str) -> bool:
        """Delete bot from registry."""
        registry = await self._load_registry()
        
        if str(user_id) not in registry or bot_name not in registry[str(user_id)]:
            return False
        
        del registry[str(user_id)][bot_name]
        
        # Remove user entry if no bots left
        if not registry[str(user_id)]:
            del registry[str(user_id)]
        
        await self._save_registry(registry)
        return True
    
    async def count_user_bots(self, user_id: int) -> int:
        """Count number of bots for a user."""
        bots = await self.get_user_bots(user_id)
        return len(bots)
