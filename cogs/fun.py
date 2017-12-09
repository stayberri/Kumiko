import discord
import requests
import datetime
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


def setup(bot):
    bot.add_cog(Fun(bot))
