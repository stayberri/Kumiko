import discord
import datetime
from discord.ext import commands


def get_friendly_avatar(user, replace_webp=True):
    """Returns a user friendly avatar url.
    This is done by replacing the size on gifs so that they can animate and if replace_webp is True (True by Default)
    .webp images are replaced with .png"""
    url = user.avatar_url
    url = url.replace("gif?size=1024", "gif")
    if replace_webp is True:
        url = url.replace(".webp", ".png")
    return url

def get_embedded_help_for(command, ctx):
    """Get the embed that correlates to the command specified.
    Returns as discord.Embed object"""
    if isinstance(command, commands.Command):
        c = command
    else:
        c = ctx.bot.all_commands.get(command)
    em = discord.Embed(color=ctx.author.color)
    em.set_author(name=f"Help for command {c.name}", icon_url=ctx.guild.me.avatar_url)
    em.add_field(name="Description", value=c.help, inline=False)
    em.add_field(name="Usage", value=f"`{ctx.prefix}{c.signature}`", inline=False)
    if len(c.aliases) > 0:
        em.add_field(name="Alias(es)", value=f"`{'`, `'.join(c.aliases)}`")
    em.add_field(name="Note",
                 value="Note that arguments surrounded with `[]` are not required while arguments surrounded by `<>` are required. Do not include either of these in the command.")
    em.set_footer(text=f"Requested by {ctx.author.display_name}",
                  icon_url=ctx.author.avatar_url.replace("?size=1024", ""))
    em.timestamp = datetime.datetime.now()
    return em