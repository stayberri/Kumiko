import discord
from discord.ext import commands
import requests
import urllib
import json
from .utils import weeb


class Image:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def owo(self, ctx):
        """Send a random owo image.
        This command is powered by weeb.sh"""
        img = weeb.request_image(type="owo")
        await ctx.send(embed=discord.Embed(title="OwO what's this?",color=ctx.author.color).set_image(url=img))

    @commands.command(aliases=["memes"])
    async def meme(self, ctx):
        """Send a random discord meme.
        This command is powered by weeb.sh"""
        await ctx.send(embed=discord.Embed(color=ctx.author.color).set_image(
            url=weeb.request_image("discord_memes")
        ))

    @commands.command()
    async def sumfuk(self, ctx):
        """Send a sumfuk image.
        This command is powered by weeb.sh"""
        await ctx.send(embed=discord.Embed(color=ctx.author.color).set_image(
            url=weeb.request_image("sumfuk")
        ))

    @commands.command()
    async def rem(self, ctx):
        """Send a Rem image.
        This command is powered by weeb.sh"""
        await ctx.send(embed=discord.Embed(color=ctx.author.color).set_image(
            url=weeb.request_image("rem")
        ))

    @commands.command()
    async def awoo(self, ctx):
        """Send an awoo image.
        This command is powered by weeb.sh"""
        await ctx.send(embed=discord.Embed(color=ctx.author.color).set_image(
            url=weeb.request_image("awoo")
        ))

    @commands.command()
    async def waifu(self, ctx):
        """Insult your waifu ;)
        This command is powered by weeb.sh"""
        await ctx.send(embed=discord.Embed(color=ctx.author.color).set_image(
            url=weeb.request_image("waifu_insult")
        ))

    @commands.command()
    async def delet(self, ctx):
        """Delet this.
        This command is powered by weeb.sh"""
        await ctx.send(embed=discord.Embed(color=ctx.author.color).set_image(
            url=weeb.request_image("delet_this")
        ))

    @commands.command()
    async def jojo(self, ctx):
        """Send a random jojo image
        This command is powered by weeb.sh"""
        await ctx.send(embed=discord.Embed(color=ctx.author.color).set_image(
            url=weeb.request_image("jojo")
        ))

    @commands.command()
    async def nani(self, ctx):
        """Omae wa mou shindeiru.
        This command is powered by weeb.sh"""
        await ctx.send(embed=discord.Embed(color=ctx.author.color).set_image(
            url=weeb.request_image("nani")
        ))

def setup(bot):
    bot.add_cog(Image(bot))