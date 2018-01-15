import discord
import platform
import requests
import datetime
import traceback
import time
import json
import hastebin
import os
from discord.ext import commands
from .utils.tools import *
from .utils import checks
from .utils import weeb

with open('config.json', 'r') as f:
    config = json.load(f)


class Info:
    def __init__(self, bot):
        self.bot = bot
        self.version = '1.1.0'

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
    async def about(self, ctx, subcommand: str = None):
        """Some stuff about me!
        Append `patreon` or `credits` to the command to get the credits and current patreon supporters."""
        if subcommand == "patreon":
            bot_hub = discord.utils.get(self.bot.guilds, id=315251940999299072)
            patron_role = discord.utils.get(bot_hub.roles, id=318113423831465984)
            em = discord.Embed(title="All Patrons (Total: {})".format(len(patron_role.members)),
                               description=", ".join([str(m) for m in patron_role.members]), color=ctx.author.color)
            await ctx.send(embed=em)
        elif subcommand == "credits":
            desc = f"**{self.bot.get_user(267207628965281792)}:** Developer (Godavaru & Kumiko)\n" \
                   + f"**{self.bot.get_user(99965250052300800)}:** Developer (Godavaru)\n" \
                   + f"**{self.bot.get_user(132584525296435200)}:** Hosting"
            em = discord.Embed(title="Credited users", description=desc, color=ctx.author.color)
            await ctx.send(embed=em)
        else:
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
            ).add_field(
                name="Support Guild",
                value="https://discord.gg/ewvvKHM"
            ).add_field(
                name="Useful Links",
                value="[Github](https://github.com/Desiiii/Kumiko), "
                      + "[Website](https://kumiko.site), and [Patreon](https://patreon.com/desii)"
            ))

    @commands.command()
    async def invite(self, ctx):
        """Gives a mobile friendly version of the invite link.

        I don't actually know if the mobile bug still exists, but it's better to be safe than sorry."""
        await ctx.send("Invite me with <https://is.gd/kumiko>!")

    @commands.command(name="help", aliases=["commands", "cmds"])
    async def _help(self, ctx, command: str = None):
        """Request help on a command or show the command list."""
        bot = self.bot
        if command is None:
            em = discord.Embed(title="Kumiko Help",
                               description=f"**{bot.description}**\n\nDo `{ctx.prefix}help <command>` without the brackets for extended help.",
                               color=ctx.author.color)
            for cog in sorted(bot.cogs, key=lambda x: x.lower()):
                cog_commands = ""
                for cmd in sorted(bot.commands, key=lambda x: x.name.lower()):
                    if cmd.cog_name == cog:
                        cog_commands += f"`{cmd}` "
                if cog == "Owner" and checks.is_dev(ctx) is False:
                    continue
                if cog_commands == "":
                    continue
                em.add_field(name=cog, value=cog_commands, inline=False)
            em.set_thumbnail(url=ctx.guild.me.avatar_url)
            em.set_footer(text=f"Total commands: {len(bot.commands)} | Requested by {ctx.author.display_name}",
                          icon_url=ctx.author.avatar_url.replace("?size=1024", ""))
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
    async def avatar(self, ctx, *, user: discord.Member = None):
        """Get the avatar of a user!
        If the user is none, it will grab your avatar. If the user is not found, this message will be shown."""
        if user is None:
            user = ctx.author
        url = get_friendly_avatar(user)
        embed = discord.Embed(
            color=ctx.author.color
        ).set_image(
            url=url
        ).set_footer(
            icon_url=get_friendly_avatar(ctx.author),
            text=f"Requested by {ctx.author.display_name}"
        ).set_author(
            icon_url=url,
            url=url,
            name=f"{user.display_name}'s avatar"
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
                fa = n * 9 / 5 - 459.67
                return f"{round(cel)} °C | {round(fa)} °F"

            def get_wind(n):
                imp = n * 2.2
                return f"{n} m/s | {round(imp)} mph"

            def get_pressure(n):
                bar = n / 1000
                return f"{round(bar)} bar | {n} hPA"

            em.add_field(
                name="🌡 Temperature",
                value=f"Current: {get_temp(j['main']['temp'])}\n"
                      + f"Max: {get_temp(j['main']['temp_max'])}\n"
                      + f"Min: {get_temp(j['main']['temp_min'])}"
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
        num = 0
        if ctx.channel.permissions_for(ctx.me).external_emojis:
            num = 1
        online = len([m.name for m in g.members if m.status == discord.Status("online")])
        idle = len([m.name for m in g.members if m.status == discord.Status("idle")])
        dnd = len([m.name for m in g.members if m.status == discord.Status("dnd")])
        try:
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
                name="Users - "+str(len(g.members)),
                value=f"{get_status_emoji('online', num)} Online: {online}\n"
                      + f"{get_status_emoji('idle', num)} Idle: {idle}\n"
                      + f"{get_status_emoji('dnd', num)} DnD: {dnd}",
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
        except:
            await ctx.send("```py\n{}\n```".format(traceback.format_exc()))

    @commands.command(aliases=["user", "uinfo"])
    async def userinfo(self, ctx, *, user: discord.Member = None):
        """Display information about a user."""
        if not user:
            user = ctx.author
        em = discord.Embed(color=user.color)
        em.add_field(name="Joined At:", value=user.joined_at.strftime("%A %d %B %Y at %H:%M:%S"), inline=False)
        em.add_field(name="Created At:", value=user.created_at.strftime("%A %d %B %Y at %H:%M:%S"), inline=False)
        em.add_field(name="Days Since Join:", value=(datetime.datetime.now() - user.joined_at).days)
        em.add_field(name="Days Since Creation:", value=(datetime.datetime.now() - user.created_at).days)
        em.add_field(name="Status:", value=user.status)
        em.add_field(name="Nickname:", value=user.nick)
        em.add_field(name="Voice Channel:", value=user.voice.channel if user.voice is not None else None)
        em.add_field(name="Is Bot:", value=user.bot)
        em.add_field(name="Game:", value=user.game, inline=False)
        em.add_field(name="Top Role:", value=user.top_role.name)
        em.add_field(name="Highest Position:", value=user.top_role.position)
        em.add_field(name=f"Roles [{len(user.roles) - 1}]:", value=", ".join(
            [r.name for r in sorted(user.roles, key=lambda x: -x.position) if not r.is_default()]))
        em.set_thumbnail(url=user.avatar_url.replace("?size=1024", ""))
        em.set_author(name=f"{user} ({user.id})", icon_url=user.avatar_url.replace("?size=1024", ""),
                      url=user.avatar_url.replace("?size=1024", ""))
        em.set_footer(text=f"Requested by {ctx.author.display_name}",
                      icon_url=ctx.author.avatar_url.replace("?size=1024", ""))
        await ctx.send(embed=em)

    @commands.command()
    async def lyrics(self, ctx, *, song: str):
        """Get lyrics to a song from the Genius API."""
        params = song.split(' -number ')
        s = params[0]
        if len(params) > 1:
            try:
                num = int(params[1]) - 1
            except ValueError:
                num = 0
        else:
            num = 0
        r = requests.get('https://api.genius.com/search?q='+s, headers={"Authorization": config['genius-token']})
        j = r.json()
        try:
            res = j['response']['hits'][num]['result']
            em = discord.Embed(description=res['full_title'], color=ctx.author.color)
            em.set_author(name="Click me for the lyrics!", url=res['url'], icon_url=res['song_art_image_thumbnail_url'])
            em.add_field(name="Artist", value=f"[{res['primary_artist']['name']}]({res['primary_artist']['url']})")
            em.add_field(name="Verified?", value=res['primary_artist']['is_verified'])
            em.set_image(url=res['header_image_url'])
            await ctx.send(embed=em)
        except IndexError:
            await ctx.send(":x: There are no more songs or the song was not found.")

    @commands.command()
    async def artist(self, ctx, *, artist):
        """Get information on a musical artist."""
        try:
            r = requests.get('https://api.genius.com/search?q=' + artist, headers={"Authorization": config['genius-token']})
            j = r.json()
            try:
                artistid = j['response']['hits'][0]['result']['primary_artist']['id']
            except (KeyError, IndexError):
                await ctx.send(":x: Whoops! I could not find that artist!")
                return
            ar = requests.get('https://api.genius.com/artists/' + str(artistid), headers={"Authorization": config['genius-token']})
            aj = ar.json()
            res = aj['response']['artist']
            em = discord.Embed(description=f"[{res['name']}]({res['url']})",
                               color=ctx.author.color)
            em.add_field(name="Alternate Names", value=", ".join(res['alternate_names']) if len(res['alternate_names']) > 0 else "None", inline=False)
            em.add_field(name="Followers", value=str(res['followers_count']))
            em.add_field(name="Facebook", value=res['facebook_name'])
            em.add_field(name="Instagram", value=res['instagram_name'])
            em.add_field(name="Twitter", value=res['twitter_name'])
            em.add_field(name="Verified?", value=res['is_verified'])
            em.add_field(name="Artist ID", value=res['id'])
            em.set_author(name="Click me to go to the artist page!", url=res['url'], icon_url=res['header_image_url'])
            em.set_image(url=res['image_url'])
            await ctx.send(embed=em)
        except:
            await ctx.send("```py\n{}\n```".format(traceback.format_exc()))

    @commands.command()
    async def jumbo(self, ctx, emote: str):
        """Get a larger version of a custom emote."""
        e = emote.split(':')
        anim = False
        if e[0] == '<a':
            anim = True
        suffix = ".png"
        if anim is True:
            suffix = ".gif"
        url = f"https://cdn.discordapp.com/emojis/{e[2].replace('>', '')}{suffix}"
        weeb.save_to_image(url=url, name=e[1] + suffix)
        await ctx.send(file=discord.File(f'./images/{e[1]}{suffix}'))
        os.remove(f'./images/{e[1]}{suffix}')

    @commands.command(aliases=["color"])
    async def colour(self, ctx, hexcode: str):
        """Show a preview of a hex colour."""
        colour = hexcode.replace('#', '')
        for char in colour:
            if char not in "abcdef0123456789":
                await ctx.send(":x: T-that's not a valid hex code!")
                return
        if len(colour) != 6:
            await ctx.send(":x: Hex codes are six characters long!")
            return
        c = discord.Color(int(colour, 16))
        em = discord.Embed(color=c)
        em.set_image(url='https://www.colorcombos.com/images/colors/' + colour + '.png')
        em.set_author(name="Here is a preview of your colour.", icon_url=get_friendly_avatar(ctx.author))
        await ctx.send(embed=em)

    @commands.command()
    async def wiki(self, ctx, page: str = "home", category: str = None):
        """Get a wiki page.

        **All Valid Pages** ```
        home
        commands
        modifiers
        options```
        **Shorthands** ```
               Shorthand | Page
        ---------------- | ----------------
        cmds             | commands
        mod              | modifiers
        opts             | options
        "format welcome" | modifiers
        settings         | options```
        **Command Categories** ```
        action
        currency
        fun
        image
        mod
        options```"""
        pages = [
            "home",
            "commands",
            "modifiers",
            "options"
        ]
        shorthands = [
            "cmds|commands",
            "mod|modifiers",
            "opts|options",
            "format welcome|modifiers",  # this will have to be invoked with `kumiko wiki "format welcome"`
            "settings|options"
        ]
        command_categories = [
            "action",
            "currency",
            "fun",
            "image",
            "info",
            "mod",
            "options"
        ]
        p = page
        for s in shorthands:
            sp = s.split('|')
            p = p.replace(sp[0], sp[1])
        if not p.lower() in pages:
            await ctx.send(":x: That is not a valid wiki page.")
            return
        if category and p != "commands":
            await ctx.send(":x: Only the commands page uses categories.")
            return
        if category is not None and category.lower() not in command_categories:
            await ctx.send(":x: That is not a documented command category.")
            return
        base_url = "https://github.com/Desiiii/Kumiko/wiki/" + titlecase(p)
        if page == "commands" and category is not None:
            base_url += "#" + category.lower()
        await ctx.send(f":ok_hand: Generated the wiki link you needed! **<{base_url}>**")


def setup(bot):
    bot.add_cog(Info(bot))


"""    @commands.group()
    async def dbl(self, ctx, *, params: str):
        \"""Get information from DBL (DiscordBotList) API.
        Valid subcommands are: `prefix`, `lib`, `username`, and `discriminator`. By default, you must mention a bot.\"""
        if ctx.invoked_subcommand is None:
            botid = params.replace('<@!', '').replace('<@', '').replace('>', '')
            try:
                int(botid)
            except:
                await ctx.send(":x: That is not a valid mention or ID.")
                return
            url = f'https://discordbots.org/api/bots/{botid}'
            r = requests.get(url)
            result = r.json()
            em = discord.Embed(color=ctx.author.color, description=result['shortdesc'])
            em.add_field(name="Library",value=result['lib'])
            em.add_field(name="Prefix",value=result['prefix'])
            em.add_field(name='ID',value=result['id'])
            em.add_field(name="Certified",value=result['certified'])
            em.add_field(name='Upvotes',value=result['points'])
            em.add_field(name='Shards', value='Not sharding' if len(result['shards']) == 0 else len(result['shards']))
            em.add_field(name='Guilds',value='Not posting' if result['serverCount'] == -1 else result['serverCount'])
"""