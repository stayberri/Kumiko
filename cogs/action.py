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
    async def pat(self, ctx, *members: discord.Member):
        """Pat a user!
        You can also specify multiple users. However, if you mention yourself, Kumiko will do the action on you."""
        if len(members) == 0 or len(ctx.message.mentions) == 0:
            await ctx.send(":x: You must mention at least one user!")
            return
        display_names = [m.display_name for m in ctx.message.mentions]
        new_array = []
        for i in display_names:
            if i not in new_array:
                new_array.append(i)
        msg = f"**{ctx.author.display_name}** is patting **{(', '.join(new_array)).replace(', '+new_array[len(new_array)-1], ' and '+new_array[len(new_array)-1])}**"
        for me in members:
            if me.id == ctx.author.id:
                msg = "***pats you***"
        weeb.save_to_image(url=weeb.request_image_as_gif(type="pat"), name="pat.gif")
        await ctx.send(content=msg, file=discord.File("./images/pat.gif"))


    @commands.command()
    async def cry(self, ctx, *members: discord.Member):
        """When you need to cry, just do it. You can also cry at a user.
        You can also specify multiple users. However, if you mention yourself, Kumiko will do the action on you."""
        if len(ctx.message.mentions) > 0:
            display_names = [m.display_name for m in ctx.message.mentions]
            new_array = []
            for i in display_names:
                if i not in new_array:
                    new_array.append(i)
            msg = f"**{ctx.author.display_name}** is crying because of **{(', '.join(new_array)).replace(', '+new_array[len(new_array)-1], ' and '+new_array[len(new_array)-1])}**!"
            for me in ctx.message.mentions:
                if me.id == ctx.author.id:
                    msg = f"**{ctx.author.display_name}** is crying!"
        else:
            msg = f"**{ctx.author.display_name}** is crying!"
        weeb.save_to_image(url=weeb.request_image_as_gif(type="cry"), name="cry.gif")
        await ctx.send(content=msg, file=discord.File("./images/cry.gif"))

def setup(bot):
    bot.add_cog(Action(bot))