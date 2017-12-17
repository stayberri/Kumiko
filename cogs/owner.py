import discord
import hastebin
import traceback
import io
import textwrap
import json
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

        toCompile = f'async def func():\n{textwrap.indent(code, "  ")}'

        try:
            exec(toCompile, env)
        except Exception as e:
            em = discord.Embed(description=f"Excecuted and errored: {e.__class__.__name__}: {e}",
                               color=0xff0000)
            em.set_author(name="Evaluated and errored",
                          icon_url=ctx.message.author.avatar_url.replace("?size=1024", ""))
            em.set_footer(text="Executed by: " + str(ctx.message.author))
            em.set_thumbnail(
                url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Red_x.svg/480px-Red_x.svg.png')
            em.add_field(name="Code", value=f"[See here.]({hastebin.post(code.encode('utf-8'))}.py)")
            return await ctx.send(embed=em)

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            em = discord.Embed(description=f"Excecuted and errored: ```py\n{value}{traceback.format_exc()}```",
                               color=0xff0000)
            em.set_author(name="Evaluated and errored",
                          icon_url=ctx.message.author.avatar_url.replace("?size=1024", ""))
            em.set_footer(text="Executed by: " + str(ctx.message.author))
            em.set_thumbnail(
                url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Red_x.svg/480px-Red_x.svg.png')
            em.add_field(name="Code", value=f"[See here.]({hastebin.post(code.encode('utf-8'))}.py)")
            await ctx.send(embed=em)
        else:
            value = stdout.getvalue()
            if ret is None or type(ret) is discord.Message:
                if value:
                    x = f"{value}"
                    self.last_result = value
                else:
                    x = "Executed successfully with no objects returned."
            else:
                x = f"Executed successfully and returned: {value}{ret}"
                self.last_result = f"{value}{ret}"
            em = discord.Embed(description=x, color=0x00ff00)
            em.set_author(name="Evaluated with success",
                          icon_url=ctx.message.author.avatar_url.replace("?size=1024", ""))
            em.set_footer(text="Executed by: " + str(ctx.message.author))
            em.set_thumbnail(url='http://www.iconsdb.com/icons/preview/green/checked-checkbox-xxl.png')
            em.add_field(name="Code", value=f"[See here.]({hastebin.post(code.encode('utf-8'))}.py)")
            await ctx.send(embed=em)

    @commands.command()
    @commands.check(is_dev)
    async def reload(self, ctx, *, extension: str):
        """Reload an extension (Bot Owner Only)"""
        try:
            self.bot.unload_extension(extension)
            self.bot.load_extension(extension)
            await ctx.send(f":ok_hand: Reloaded module `{extension}`")
        except Exception as e:
            await ctx.send(f":sob: I-I'm sorry, I couldn't reload the `{extension}` module >w< "
                           + f"```py\n{traceback.format_exc()}```")


def setup(bot):
    bot.add_cog(Owner(bot))
