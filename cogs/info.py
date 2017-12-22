import discord
import platform
import requests
import datetime
import time
import json
from discord.ext import commands
from .utils.tools import *
from .utils import checks

with open('config.json', 'r') as f:
    config = json.load(f)

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
                       + f" ========[ Kumiko Info ]========\n"
                       + f"\n"
                       + f"Commands          : {len(self.bot.commands)}\n"
                       + f"Cogs              : {len(self.bot.cogs)}\n"
                       + f"Python Version    : {platform.python_version()}\n"
                       + f"DiscordPY Version : {discord.__version__}\n"
                       + f"Bot Version       : {self.version}\n"
                       + f"\n"
                       + f" ========[ Technical Info ]========\n"
                       + f"\n"
                       + f"Guilds            : {len(self.bot.guilds)}\n"
                       + f"Channels          : {channel_count}\n"
                       + f"Users             : {user_count}\n"
                       + f"Hostname          : {platform.node()}\n"
                       + f"OS                : {platform.system()}\n"
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
            value=self.version
        ).add_field(
            name="Guilds",
            value=str(len(self.bot.guilds))
        ).add_field(
            name="Invite",
            value="[Click here!](https://discordapp.com/api/oauth2/authorize?client_id=315297886613012481&permissions="
                  + "471198870&scope=bot) If you need a non-embed link, use `{}invite`!".format(ctx.prefix)
        ))

    @commands.command()
    async def invite(self, ctx):
        """Gives a mobile friendly version of the invite link.

        I don't actually know if the mobile bug still exists, but it's better to be safe than sorry."""
        await ctx.send("Invite me with <https://is.gd/kumiko>!")

    @commands.command(name="help")
    async def _help(self, ctx, command: str = None):
        """Request help on a command or show the command list."""
        bot = self.bot
        if command is None:
            em = discord.Embed(title="Kumiko Help", description=f"**{bot.description}**\n\nDo `{ctx.prefix}help <command>` without the brackets for extended help.", color=ctx.author.color)
            for cog in sorted(bot.cogs, key=lambda x: x.lower()):
                cog_commands = ""
                for cmd in sorted(bot.commands, key=lambda x: x.name.lower()):
                    if cmd.cog_name == cog:
                        cog_commands += f"`{cmd}` "
                if cog == "Owner" and checks.is_dev(ctx) is False:
                    continue
                em.add_field(name=cog, value=cog_commands, inline=False)
            em.set_thumbnail(url=ctx.guild.me.avatar_url)
            em.set_footer(text=f"Total commands: {len(bot.commands)} | Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url.replace("?size=1024", ""))
            em.timestamp = datetime.datetime.now()
        else:
            c = bot.all_commands.get(command)
            if c is None:
                await ctx.send(":x: That is not a command.")
                return
            em = get_embedded_help_for(c, ctx)
        await ctx.send(embed=em)

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
        em.add_field(name="Example", value=example, inline=False)
        em.add_field(name="👍", value=request['thumbs_up'], inline=True)
        em.add_field(name="👎", value=request['thumbs_down'], inline=True)
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

    @commands.command()
    async def avatar(self, ctx, user: discord.Member = None):
        """Get the avatar of a user!
        If the user is none, it will grab your avatar. If the user is not found, this message will be shown."""
        if user is None:
            user = ctx.author
        url = get_friendly_avatar(user)
        embed = discord.Embed(
            title=f"{user.display_name}'s avatar"
        ).set_image(
            url=url
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def weather(self, ctx, *, city: str):
        """Get weather information for a specified city."""
        r = requests.get(f"http://api.openweathermap.org/data/2.5/weather/?q={city}&APPID={config['weather-token']}")
        if r.text.startswith('{"coord"'):
            j = r.json()
            em = discord.Embed(
                title=f":flag_{j['sys']['country'].lower()}: Weather for {j['name']}, {j['sys']['country']}",
                description=f"{j['weather'][0]['main']} ({j['clouds']['all']}% clouds)",
                color=ctx.author.color
            )
            def get_temp(n):
                cel = n - 273.15
                fa = n * 9/5 - 459.67
                return f"{round(cel)} °C | {round(fa)} °F"
            def get_wind(n):
                imp = n * 2.2
                return f"{n} m/s | {round(imp)} mph"
            def get_pressure(n):
                bar = n / 1000
                return f"{round(bar)} bar | {n} hPA"
            em.add_field(
                name="🌡 Temperature",
                value=f"Current: {get_temp(j['main']['temp'])}\nMax: {get_temp(j['main']['temp_max'])}\nMin: {get_temp(j['main']['temp_min'])}"
            ).add_field(
                name="💧 Humidity",
                value=f"{j['main']['humidity']}%"
            ).add_field(
                name="💨 Wind Speeds",
                value=get_wind(j['wind']['speed'])
            ).add_field(
                name="🎐 Pressure",
                value=get_pressure(j['main']['pressure'])
            ).set_thumbnail(
                url=f"http://openweathermap.org/img/w/{j['weather'][0]['icon']}.png"
            )
            await ctx.send(embed=em)
        else:
            await ctx.send(":x: U-uh, I'm sorry, but that c-city doesn't seem to exist!")

    @commands.command(aliases=["guild", "ginfo", "server", "serverinfo", "sinfo"])
    async def guildinfo(self, ctx):
        """Get information on the guild you are currently in!"""
        g = ctx.guild
        guild_embed = discord.Embed(
            title=g.name,
            description=f"Guild ID: {g.id}",
            color=ctx.author.color
        ).set_thumbnail(
            url=g.icon_url
        ).add_field(
            name="Created At",
            value=g.created_at.strftime("%A %d %B %Y at %H:%M:%S"),
            inline=False
        ).add_field(
            name="Days Since Creation",
            value=(datetime.datetime.now() - g.created_at).days
        ).add_field(
            name="Guild Region:",
            value=g.region
        ).add_field(
            name="AFK Timeout",
            value=f"{int(g.afk_timeout/60)} minutes"
        ).add_field(
            name="Owner",
            value=str(g.owner)
        ).add_field(
            name="Total Channels",
            value=len(g.channels)
        ).add_field(
            name="Category Channels",
            value=len([c.name for c in g.channels if isinstance(c, discord.CategoryChannel)])
        ).add_field(
            name="Text Channels",
            value=len([c.name for c in g.channels if isinstance(c, discord.TextChannel)])
        ).add_field(
            name="Voice Channels",
            value=len([c.name for c in g.channels if isinstance(c, discord.VoiceChannel)])
        ).add_field(
            name="Verification Level",
            value=g.verification_level
        ).add_field(
            name="Explicit Content Filter",
            value=g.explicit_content_filter
        ).add_field(
            name=f"Roles - {len(g.roles)-1}",
            value=", ".join([r.name for r in sorted(g.roles, key=lambda x: -x.position) if not r.is_default()])
        )
        await ctx.send(embed=guild_embed)


def setup(bot):
    bot.add_cog(Info(bot))
