"""Bot configuration file."""

from functools import lru_cache
from zoneinfo import ZoneInfo

from pydantic import BaseSettings

class Settings(BaseSettings):
    """Bot configuration class."""
    bot_name: str = "Axin"
    bot_token: str = ""
    guild_id: int = 0

    mongo_db: str = ""
    db_name: str = ""
    questions_collection: str = ""

    timezone = ZoneInfo("Asia/Kolkata")

    class Config:
        """BaseSettings config"""
        env_file = ".env"


@lru_cache()
def get_config():
    """Returns the config object (Cached)."""
    return Settings()
