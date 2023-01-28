"""Discord Bot Main."""

from discord.ext import commands

from bot.commands import ping, set_dailyquest
from bot.config import get_config
from bot.scheduler import scheduler
from bot.web import keep_alive


config = get_config()
bot = commands.Bot()
bot.add_application_command(ping)
bot.add_application_command(set_dailyquest)


@bot.event
async def on_ready():
    """On Bot Ready Event."""

    print("Bot is Ready")
    scheduler.start()
    keep_alive()

bot.run(config.bot_token)
