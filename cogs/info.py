import discord
import platform
from discord.ext import commands


class Info():
    def __init__(self, bot):
        self.bot = bot
        self.version = '1.0.0_'

    @commands.command()
    async def info(self, ctx):
        """Statistical information about the bot."""
        await ctx.send("```prolog\n"
                       + f" ----- Kumiko Info -----\n"
                       + f"Commands: {len(self.bot.commands)}\n"
                       + f"Cogs: {len(self.bot.cogs)}\n"
                       + f"DiscordPY Version: {platform.python_version()}\n"
                       + f"Bot Version : {self.version}\n"
                       + f"\n"
                       + f" ----- Technical Info -----\n"
                       + f"Guilds: {len(self.bot.guilds)}")