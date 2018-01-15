import discord
import datetime
import aiohttp
import json
from os import path
from discord.ext import commands

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "..", "..", "config.json"))
with open(filepath, 'r') as f:
    config = json.load(f)


def get_friendly_avatar(user, replace_webp=True):
    """Returns a user friendly avatar url.
    This is done by replacing the size on gifs so that they can animate and if replace_webp is True (True by Default)
    .webp images are replaced with .png"""
    url = user.avatar_url
    url = url.replace("gif?size=1024", "gif?size=1024&.gif")
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
    sig = c.signature.split(' ')
    cmd = sig[0].replace('[', '').split('|')
    usage = c.signature.replace(sig[0], "")[1:]
    em = discord.Embed(color=ctx.author.color)
    em.set_author(name=f"Help for command {c.name}", icon_url=ctx.guild.me.avatar_url)
    em.add_field(name="Description", value=c.help, inline=False)
    em.add_field(name="Usage", value=f"`{ctx.prefix}{cmd[0]} {usage}`", inline=False)
    if len(c.aliases) > 0:
        em.add_field(name="Alias(es)", value=f"`{'`, `'.join(c.aliases)}`")
    em.add_field(name="Note",
                 value="Note that arguments surrounded with `[]` are not required while arguments surrounded by `<>` "
                       + "are required. Do not include either of these in the command.")
    em.set_footer(text=f"Requested by {ctx.author.display_name}",
                  icon_url=ctx.author.avatar_url.replace("?size=1024", ""))
    em.timestamp = datetime.datetime.now()
    return em


def remove_html(string):
    return string.replace('&amp;', '&').replace("&lt;", '<').replace("&gt;", '>').replace('&quot;', '"').replace(
        '&#039;', "'")


async def post_guild_count(count, botid):
    api_url = f"https://discordbots.org/api/bots/{botid}/stats"
    async with aiohttp.ClientSession() as session:
        await session.post(api_url, data={'server_count': count}, headers={'Authorization': config['dbltoken']})


def parse_modifiers(string, user, guild):
    """Parses the modifers in the given string with the user and guild objects that are provided."""
    parsed_string = string.replace("{user}", str(user)).replace("{user.name}", user.name).replace("{user.id}", str(user.id))\
        .replace("{user.discriminator}", str(user.discriminator)).replace("{user.mention}", user.mention)\
        .replace("{guild}", guild.name).replace("{guild.name}", guild.name).replace("{guild.id}", str(guild.id))\
        .replace("{guild.owner}", str(guild.owner)).replace("{guild.owner.name}", guild.owner.name)\
        .replace("{guild.owner.discriminator}", str(guild.owner.discriminator)).replace("{guild.owner.id}", str(guild.owner.id))\
        .replace("{guild.owner.mention}", guild.owner.mention)
    return parsed_string


def titlecase(string):
    """Makes the first letter of the string capital with all others as lowercase."""
    capital = string[0].upper()
    lower = string[1:].lower()
    return capital + lower


def get_status_emoji(status, number):
    if status == "online":
        array = [
                "💚",
                "<:online:398856032392183819>"
            ]
    elif status == "idle":
        array = [
                "💛",
                "<:idle:398856031360253962>"
            ]
    elif status == 'dnd':
        array = [
                "❤",
                "<:dnd:398856030068670477>"
            ]
    return str(array[number])
