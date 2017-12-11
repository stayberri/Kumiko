import discord
import platform
import requests
import datetime
import time
import json
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
        """Some stuff about me!"""
        desc = "H-hello! My name is **Kumiko** and I am a multi-purpose Discord Bot made by " \
               + "**Desiree#3658** in Python. " \
               + "I-I have uh many features that you can choose from, m-mostly some fun commands to keep you occupied. " \
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

    @commands.command()
    async def urban(self, ctx, *, params):
        """Search up a word on urban dictionary.
        To get another result for the same argument, simply use `urban <word> -number <int>`"""
        params = params.split(' -number ')
        word = params[0]
        if len(params) > 1:
            try:
                num = int(params[1]) - 1
            except:
                await ctx.send(":x: You gave me an improper number!")
                return
        else:
            num = 0
        r = requests.get(f"http://api.urbandictionary.com/v0/define?term={word}")
        j = r.json()
        try:
            request = j['list'][num]
        except IndexError:
            await ctx.send(":x: There are no more results.")
            return
        definition = request['definition']
        if len(definition) > 1000:
            definition = definition[997:] + "..."
        if definition == "":
            definition = "None"
        example = request['example']
        if len(example) > 1000:
            example = example[997:] + "..."
        if example == "":
            example = "None"
        em = discord.Embed(description=f"Definition #{num+1}", color=ctx.author.color)
        em.add_field(name="Definition", value=definition, inline=False)
        em.add_field(name="Example", value=example)
        em.set_author(name=f"Urban dictionary definition for {word}", url=request['permalink'])
        em.set_footer(text=f"Author: {request['author']}")
        await ctx.send(embed=em)

    @commands.command()
    async def ping(self, ctx):
        """Check my response time and my websocket ping"""
        before = datetime.datetime.utcnow()
        ping_msg = await ctx.send(":mega: Baka! Don't look at me when I'm pinging!")
        ping = (datetime.datetime.utcnow() - before) * 1000
        before2 = time.monotonic()
        await (await self.bot.ws.ping())
        after = time.monotonic()
        ping2 = (after - before2) * 1000
        await ping_msg.edit(content=":mega: W-wew! I responded in **{:.0f}ms**!".format(
            ping.total_seconds()) + " `Websocket: {0:.0f}ms`".format(ping2))


def setup(bot):
    bot.add_cog(Info(bot))
