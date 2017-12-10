import discord
import platform
from discord.ext import commands


class Info():
    def __init__(self, bot):
        self.bot = bot
        self.version = '1.0.0'

    @commands.command()
    async def info(self, ctx):
        """Statistical information about the bot.

        Note the command is unfinished 👌"""
        channel_count = 0
        user_count = 0
        for g in self.bot.guilds:
            for _ in g.channels:
                channel_count += 1
            for _ in g.members:
                user_count += 1
        await ctx.send("```prolog\n"
                       + f" ----- Kumiko Info -----\n"
                       + f"Commands: {len(self.bot.commands)}\n"
                       + f"Cogs: {len(self.bot.cogs)}\n"
                       + f"DiscordPY Version: {platform.python_version()}\n"
                       + f"Bot Version : {self.version}\n"
                       + f"\n"
                       + f" ----- Technical Info -----\n"
                       + f"Guilds: {len(self.bot.guilds)}\n"
                       + f"Channels: {channel_count}\n"
                       + f"Users: {user_count}"
                       + f"```")

    @commands.command()
    async def about(self, ctx):
        desc = "H-hello! My name is **Kumiko** and I am a multi-purpose Discord Bot made by "\
               + "**Desiree#3658** in Python. "\
               + "I-I have uh many features that you can choose from, m-mostly some fun commands to keep you occupied. "\
               + "I-I mean, it's n-not like I w-want to make sure you have fun or anything... baka!"
        await ctx.send(embed=discord.Embed(
            title="About Me",
            description=desc,
            color=ctx.author.color
        ).add_field(
            name="Version",
            value=self.version,
            inline=False
        ).add_field(
            name="Guilds",
            value=str(len(self.bot.guilds)),
            inline=False
        ))


def setup(bot):
    bot.add_cog(Info(bot))
