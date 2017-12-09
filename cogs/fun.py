import discord
import requests
import datetime
import random
import asyncio
import json
from discord.ext import commands


class Fun():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="8ball")
    async def _8ball(self, ctx, *, question):
        """Consult the magic 8ball with a question!"""
        url = 'https://8ball.delegator.com/magic/JSON/' + question
        r = requests.get(url)
        j = r.json()
        q = j['magic']['question']
        a = j['magic']['answer']
        t = j['magic']['type']
        em = discord.Embed(description=f"**Question:** {q}\n**Answer:** {a}\n**Response Type:** {t}", color=0x00ff00)
        em.set_thumbnail(url="https://8ball.delegator.com/images/8ball.png")
        em.set_author(name="You consult the magic 8 ball...", icon_url=ctx.author.avatar_url.replace("?size=1024", ""))
        em.set_footer(text="Powered by 8ball.delegator.com")
        em.timestamp = datetime.datetime.now()
        await ctx.send(embed=em)

    @commands.command()
    async def bowling(self, ctx):
        """Play a round of bowling!"""
        init = random.choice(range(11))
        if init == 10:
            await ctx.send(":bowling: Strike! You got all of the pins!")
        else:
            await ctx.send(
                ":bowling: You tried to get a strike, but you ended up getting **{}** pins instead. Let's try again.".format(
                    init))
            second = random.choice(range(10 - init))
            if init + second == 10:
                await ctx.send(":bowling: You got a spare! ({} then {})".format(init, second))
            else:
                await ctx.send(
                    ":bowling: You didn't win, but you knocked down **{}** pins! ({} then {})".format(init + second,
                                                                                                      init, second))


def setup(bot):
    bot.add_cog(Fun(bot))
