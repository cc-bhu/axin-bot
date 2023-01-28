"""Commands for the bot."""

import discord
from discord.ext import commands

from bot.scheduler import scheduler
from bot.internal.dailyquest import send_dailyquest
from bot.config import get_config

config = get_config()
GUILD_ID = config.guild_id


@discord.slash_command(name="ping", guild_ids=[GUILD_ID])
async def ping(ctx):
    """Ping the bot."""
    await ctx.respond(f"Hey, I am {config.bot_name}.")


@discord.slash_command(name="dailyquest", guild_ids=[GUILD_ID])
@commands.has_any_role("root", "lead")
async def set_dailyquest(
    ctx: discord.ApplicationContext,
    command: discord.Option(str, "command", choices=["schedule", "stop"]),
    channel: discord.TextChannel,
    hour: str = "00", minute: str = "00"
):
    """Schedule Daily Quest."""

    if command.lower() == "schedule":

        scheduler.add_job(
            send_dailyquest, trigger="cron", hour=hour, minute=minute,
            args=[channel.id], id="dailyquest", name="dailyquest",
            replace_existing=True
        )
        await ctx.respond(f"Daily Quest Scheduled every day at {hour}:{minute}")

    elif command.lower() == "stop":
        scheduler.pause_job("dailyquest")
        await ctx.respond("Daily Quest Stopped")


@set_dailyquest.error
async def exception_handler(ctx: discord.ApplicationContext, error: Exception):
    """Handle exceptions for bot."""
    if isinstance(error, commands.MissingAnyRole):
        await ctx.respond("you are not allowed to use this command.")
