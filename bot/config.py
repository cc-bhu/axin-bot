"""Bot configuration file."""

from functools import lru_cache

from pydantic import BaseSettings
from pytz import timezone

class Settings(BaseSettings):
    """Bot configuration class."""
    bot_name: str = "Axin"
    bot_token: str = ""
    guild_id: int = 0

    mongo_db: str = ""
    db_name: str = ""
    questions_collection: str = ""

    timezone = timezone("Asia/Kolkata")

    class Config:
        """BaseSettings config"""
        env_file = ".env"


@lru_cache()
def get_config():
    """Returns the config object (Cached)."""
    return Settings()
