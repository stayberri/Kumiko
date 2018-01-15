import discord
import json
import requests
import urllib
from discord.ext import commands
from .utils import weeb


class Action:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pat(self, ctx, *members: str):
        """Pat a user!
        You can also specify multiple users. However, if you mention yourself, Kumiko will do the action on you."""
        l = []
        for m in members:
            if m.startswith('<@') and m.endswith('>'):
                mid = m.replace('<@!', '').replace('<@', '').replace('>', '')
                try:
                    mem = ctx.guild.get_member(int(mid))
                    if mem is None or mem.display_name in l:
                        continue
                    else:
                        l.append(ctx.guild.get_member(int(mid)).display_name)
                except:
                    continue
        if len(l) == 0:
            await ctx.send(":x: You must mention at least one user.")
            return
        msg = f"**{ctx.author.display_name}** is patting **{(', '.join(l)).replace(', '+l[len(l)-1], ' and '+l[len(l)-1])}**"
        for u in l:
            if u == ctx.author.display_name:
                msg = f'***pats you***'
        weeb.save_to_image(url=weeb.request_image_as_gif(type="pat"), name="pat.gif")
        await ctx.send(content=msg, file=discord.File("./images/pat.gif"))

    @commands.command()
    async def cry(self, ctx, *members: str):
        """When you need to cry, just do it. You can also cry at a user.
        You can also specify multiple users. However, if you mention yourself, Kumiko will do the action on you."""
        if len(members) > 0:
            l = []
            for m in members:
                if m.startswith('<@') and m.endswith('>'):
                    mid = m.replace('<@!', '').replace('<@', '').replace('>', '')
                    try:
                        mem = ctx.guild.get_member(int(mid))
                        if mem is None or mem.display_name in l:
                            continue
                        else:
                            l.append(ctx.guild.get_member(int(mid)).display_name)
                    except:
                        continue
            msg = f"**{ctx.author.display_name}** is crying because of **{(', '.join(l)).replace(', '+l[len(l)-1], ' and '+l[len(l)-1])}**."
            for v in l:
                if v == ctx.author.display_name:
                    msg = f"**{ctx.author.display_name}** is crying!"
        else:
            msg = f"**{ctx.author.display_name}** is crying!"
        weeb.save_to_image(url=weeb.request_image_as_gif(type="cry"), name="cry.gif")
        await ctx.send(content=msg, file=discord.File("./images/cry.gif"))

    @commands.command()
    async def kiss(self, ctx, *members: str):
        """Kiss a user!
        You can also specify multiple users. However, if you mention yourself, Kumiko will do the action on you."""
        l = []
        for m in members:
            if m.startswith('<@') and m.endswith('>'):
                mid = m.replace('<@!', '').replace('<@', '').replace('>', '')
                try:
                    mem = ctx.guild.get_member(int(mid))
                    if mem is None or mem.display_name in l:
                        continue
                    else:
                        l.append(ctx.guild.get_member(int(mid)).display_name)
                except:
                    continue
        if len(l) == 0:
            await ctx.send(":x: You must mention at least one user.")
            return
        msg = f"**{ctx.author.display_name}** is kissing **{(', '.join(l)).replace(', '+l[len(l)-1], ' and '+l[len(l)-1])}**"
        for u in l:
            if u == ctx.author.display_name:
                msg = "Aww, you don't have anyone to kiss you? I'll do it! :kissing_heart:"
        weeb.save_to_image(url=weeb.request_image_as_gif(type="kiss"), name="kiss.gif")
        await ctx.send(content=msg, file=discord.File("./images/kiss.gif"))

    @commands.command()
    async def hug(self, ctx, *members: str):
        """Hug a user!
        You can also specify multiple users. However, if you mention yourself, Kumiko will do the action on you."""
        l = []
        for m in members:
            if m.startswith('<@') and m.endswith('>'):
                mid = m.replace('<@!', '').replace('<@', '').replace('>', '')
                try:
                    mem = ctx.guild.get_member(int(mid))
                    if mem is None or mem.display_name in l:
                        continue
                    else:
                        l.append(ctx.guild.get_member(int(mid)).display_name)
                except:
                    continue
        if len(l) == 0:
            await ctx.send(":x: You must mention at least one user.")
            return
        msg = f"**{ctx.author.display_name}** is hugging **{(', '.join(l)).replace(', '+l[len(l)-1], ' and '+l[len(l)-1])}**"
        for u in l:
            if u == ctx.author.display_name:
                msg = f"*hugs* Are you feeling better, **{ctx.author.display_name}**"
        weeb.save_to_image(url=weeb.request_image_as_gif(type="hug"), name="hug.gif")
        await ctx.send(content=msg, file=discord.File("./images/hug.gif"))

    @commands.command()
    async def cuddle(self, ctx, *members: str):
        """Cuddle with a user!
        You can also specify multiple users. However, if you mention yourself, Kumiko will do the action on you."""
        l = []
        for m in members:
            if m.startswith('<@') and m.endswith('>'):
                mid = m.replace('<@!', '').replace('<@', '').replace('>', '')
                try:
                    mem = ctx.guild.get_member(int(mid))
                    if mem is None or mem.display_name in l:
                        continue
                    else:
                        l.append(ctx.guild.get_member(int(mid)).display_name)
                except:
                    continue
        if len(l) == 0:
            await ctx.send(":x: You must mention at least one user.")
            return
        msg = f"**{ctx.author.display_name}** is cuddling with **{(', '.join(l)).replace(', '+l[len(l)-1], ' and '+l[len(l)-1])}**"
        for u in l:
            if u == ctx.author.display_name:
                msg = "Aww, you don't have anyone to cuddle with you? I'll do it!"
        weeb.save_to_image(url=weeb.request_image_as_gif(type="cuddle"), name="cuddle.gif")
        await ctx.send(content=msg, file=discord.File("./images/cuddle.gif"))

    @commands.command()
    async def stare(self, ctx, *members: str):
        """Stare at a user!
        You can also specify multiple users. However, if you mention yourself, Kumiko will do the action on you."""
        l = []
        for m in members:
            if m.startswith('<@') and m.endswith('>'):
                mid = m.replace('<@!', '').replace('<@', '').replace('>', '')
                try:
                    mem = ctx.guild.get_member(int(mid))
                    if mem is None or mem.display_name in l:
                        continue
                    else:
                        l.append(ctx.guild.get_member(int(mid)).display_name)
                except:
                    continue
        if len(l) == 0:
            await ctx.send(":x: You must mention at least one user.")
            return
        msg = f"**{ctx.author.display_name}** is staring at **{(', '.join(l)).replace(', '+l[len(l)-1], ' and '+l[len(l)-1])}**"
        for u in l:
            if u == ctx.author.display_name:
                msg = "***stares at you***"
        weeb.save_to_image(url=weeb.request_image_as_gif(type="stare"), name="stare.gif")
        await ctx.send(content=msg, file=discord.File("./images/stare.gif"))

    @commands.command()
    async def think(self, ctx, *members: str):
        """Thonk.
        You can also specify multiple users. However, if you mention yourself, Kumiko will do the action on you."""
        if len(members) > 0:
            l = []
            for m in members:
                if m.startswith('<@') and m.endswith('>'):
                    mid = m.replace('<@!', '').replace('<@', '').replace('>', '')
                    try:
                        mem = ctx.guild.get_member(int(mid))
                        if mem is None or mem.display_name in l:
                            continue
                        else:
                            l.append(ctx.guild.get_member(int(mid)).display_name)
                    except:
                        continue
            for v in l:
                if v == ctx.author.display_name:
                    msg = f"**{ctx.author.display_name}** is thinking..."
                else:
                    msg = f"**{ctx.author.display_name}** thinking about **{(', '.join(l)).replace(', '+l[len(l)-1], ' and '+l[len(l)-1])}**!"
        else:
            msg = f"**{ctx.author.display_name}** is thinking..."
        weeb.save_to_image(url=weeb.request_image_as_gif(type="thinking"), name="think.gif")
        await ctx.send(content=msg, file=discord.File("./images/think.gif"))


def setup(bot):
    bot.add_cog(Action(bot))