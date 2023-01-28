"""Discord API."""

import asyncio
from typing import Optional

from discord.http import HTTPClient
from discord.types.message import Message
from discord.types.threads import ThreadArchiveDuration

from bot.config import get_config

config = get_config()
loop = asyncio.get_event_loop()

client = HTTPClient(loop=loop)
loop.run_until_complete(
    client.static_login(config.bot_token)
)

async def send_message(
    _id: int,
    text: str,
    thread_name: Optional[str] = None,
) -> Message:
    """Send a message to a channel."""

    message = await client.send_message(_id, text)

    if thread_name:
        channel = await client.get_channel(_id)
        archive_duration: ThreadArchiveDuration = channel.get(
            "default_auto_archive_duration", 1440
        )
        thread = await client.start_thread_with_message(
            channel_id=_id, message_id=message["id"], name=thread_name,
            auto_archive_duration=archive_duration,
        )
        message["thread"] = thread

    return message
