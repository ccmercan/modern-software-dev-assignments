"""
Configuration management for the application.
Handles environment variables, paths, and application settings.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    def __init__(self):
        # Database settings
        self.db_path: Optional[str] = os.getenv("DB_PATH")
        self.data_dir: Optional[str] = os.getenv("DATA_DIR")
        
        # Ollama settings
        self.ollama_model: str = os.getenv("OLLAMA_MODEL", "qwen3:1.7b")
        self.ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        # Application settings
        self.app_title: str = os.getenv("APP_TITLE", "Action Item Extractor")
        self.debug: bool = os.getenv("DEBUG", "false").lower() in ("true", "1", "yes")


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


def get_base_dir() -> Path:
    """Get the base directory of the project."""
    return Path(__file__).resolve().parents[1]


def get_data_dir() -> Path:
    """Get the data directory path."""
    settings = get_settings()
    if settings.data_dir:
        return Path(settings.data_dir).expanduser().resolve()
    return get_base_dir() / "data"


def get_db_path() -> Path:
    """Get the database file path."""
    settings = get_settings()
    if settings.db_path:
        return Path(settings.db_path).expanduser().resolve()
    return get_data_dir() / "app.db"


def get_frontend_dir() -> Path:
    """Get the frontend directory path."""
    return get_base_dir() / "frontend"
