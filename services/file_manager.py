"""File system management for generated bots."""

from pathlib import Path
from typing import Dict
import aiofiles

from config import BOTS_DIR


class FileManager:
    """Manages bot file creation and structure."""
    
    def __init__(self):
        self.bots_dir = BOTS_DIR
        self.bots_dir.mkdir(exist_ok=True)
    
    def get_bot_dir(self, bot_name: str) -> Path:
        """Get directory path for a bot."""
        return self.bots_dir / bot_name
    
    async def create_bot_directory(self, bot_name: str) -> Path:
        """Create directory structure for a bot."""
        bot_dir = self.get_bot_dir(bot_name)
        bot_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (bot_dir / "handlers").mkdir(exist_ok=True)
        (bot_dir / "services").mkdir(exist_ok=True)
        (bot_dir / "utils").mkdir(exist_ok=True)
        
        return bot_dir
    
    async def write_file(self, file_path: Path, content: str):
        """Write content to a file."""
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
            await f.write(content)
    
    async def write_files(self, bot_name: str, files: Dict[str, str]):
        """Write multiple files for a bot."""
        bot_dir = self.get_bot_dir(bot_name)
        
        for file_path, content in files.items():
            full_path = bot_dir / file_path
            await self.write_file(full_path, content)
    
    def bot_exists(self, bot_name: str) -> bool:
        """Check if bot directory exists."""
        return self.get_bot_dir(bot_name).exists()
    
    async def cleanup_bot(self, bot_name: str):
        """Remove bot directory (use with caution)."""
        bot_dir = self.get_bot_dir(bot_name)
        if bot_dir.exists():
            import shutil
            shutil.rmtree(bot_dir)
