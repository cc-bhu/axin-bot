"""Utility functions for the bot."""

import discord
from discord.ext import commands

from main import set_dailyquest


@set_dailyquest.error
async def exception_handler(ctx: discord.ApplicationContext, error: Exception):
    """Handle exceptions for bot."""
    if isinstance(error, commands.MissingAnyRole):
        await ctx.respond("you are not allowed to use this command.")
