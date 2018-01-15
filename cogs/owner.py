import discord
import hastebin
import traceback
import io
import textwrap
import json
import requests
import pymysql
from contextlib import redirect_stdout
from discord.ext import commands
from .utils.checks import *


class Owner():
    def __init__(self, bot):
        self.bot = bot
        self.last_result = None

    @commands.command(name="eval")
    @commands.check(is_dev)
    async def _eval(self, ctx, *, code):
        """Evaluate code. (Bot Owner Only)"""
        env = {
            'self': self,
            'bot': self.bot,
            'client': self.bot,
            'ctx': ctx,
            'message': ctx.message,
            'guild': ctx.guild,
            'channel': ctx.channel,
            'author': ctx.author,
            'me': ctx.me,
            'that': self.last_result
        }
        env.update(globals())

        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(code, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f"```py\n{e.__class__.__name__}: {e}```")

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception:
            await ctx.send(f"```py\n{traceback.format_exc()}```")
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    x = f"{value}"
                    self.last_result = value
                else:
                    x = "Executed successfully with no objects returned."
            else:
                x = f"Executed successfully and returned: ```py\n{value}{ret}```"
                self.last_result = ret
            await ctx.send(x)

    @commands.command()
    @commands.check(is_dev)
    async def reload(self, ctx, *, extension: str):
        """Reload an extension (Bot Owner Only)"""
        try:
            self.bot.unload_extension('cogs.' + extension)
            self.bot.load_extension('cogs.' + extension)
            await ctx.send(f":ok_hand: Reloaded /cogs/{extension}.py")
        except Exception as e:
            await ctx.send(f":sob: I-I'm sorry, I couldn't reload the `{extension}` module >w< "
                           + f"```py\n{traceback.format_exc()}```")

    @commands.command()
    @commands.check(is_dev)
    async def unload(self, ctx, *, extension: str):
        """Unload an extension (Bot Owner Only)"""
        self.bot.unload_extension("cogs." + extension)
        await ctx.send(f":ok_hand: Unloaded /cogs/{extension}.py")

    @commands.command()
    @commands.check(is_dev)
    async def load(self, ctx, *, extension: str):
        """Load an extension (Bot Owner Only)"""
        try:
            self.bot.load_extension("cogs." + extension)
            await ctx.send(f":ok_hand: Loaded /cogs/{extension}.py")
        except Exception as e:
            await ctx.send(f":sob: I-I'm sorry, I couldn't load the `{extension}` module >w< "
                           + f"```py\n{traceback.format_exc()}```")


def setup(bot):
    bot.add_cog(Owner(bot))
