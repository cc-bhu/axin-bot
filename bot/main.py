"""Bot Interaction Interface."""

from datetime import datetime, timedelta
from string import Template

import discord
from discord.ext import commands

from internal import get_question
from config import get_config
from scheduler import scheduler, add_job
from templates.message import DAILYQUEST_TEMPALTE, DAILYQUEST_HINT_TEMPALTE
from web import keep_alive


config = get_config()

GUILD_ID = config.guild_id
bot = commands.Bot()


@bot.slash_command(name="ping", guild_ids=[GUILD_ID])
async def ping(ctx):
    """Ping the bot."""

    await ctx.respond(f"Hey, I am {config.bot_name}.")


@bot.slash_command(name="dailyquest", guild_ids=[GUILD_ID])
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
            dailyquest, trigger="cron", hour=hour, minute = minute,
            args=[channel.id], id="dailyquest", name="dailyquest",
            replace_existing=True
        )
        await ctx.respond(f"Daily Quest Scheduled every day at {hour}:{minute}")

    elif command.lower() == "stop":
        scheduler.pause_job("dailyquest")
        await ctx.respond("Daily Quest Stopped")


async def send_message(_id: int, message: str) -> discord.Message:
    """Send Message to a channel/thread."""

    channel = bot.get_channel(_id)
    return (await channel.send(message))


async def dailyquest(channel_id: int):
    """Send Daily Quest Message."""

    # Get Question
    question = await get_question(level="easy", success=65)

    # Generate Message
    message = Template(DAILYQUEST_TEMPALTE).substitute(
        title=question.title,
        description=question.description,
        slug=question.slug,
    )

    # Send Message
    message = await send_message(channel_id, message)

    # Create Thread
    thread = await message.create_thread(name=question.title)
    await thread.send("Discussion Thread")

    if question.hint:
        print("Hint Present")
        hint = Template(DAILYQUEST_HINT_TEMPALTE).substitute(hint=question.hint)
        add_job(
            send_message,
            datetime.now() + timedelta(hours=20),
            args=[thread.id, hint]
        )


@bot.event
async def on_ready():
    """On Bot Ready Event."""

    print("Bot is Ready")
    scheduler.start()
    keep_alive()

bot.run(config.bot_token)
