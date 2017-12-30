import discord
from discord.ext import commands
import pymysql
import json
from .utils.checks import *
from .utils.db import *
from .utils.tools import *

with open('config.json', 'r') as f:
    config = json.load(f)


class Options:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(can_manage_guild)
    async def disable(self, ctx, *, channel: discord.TextChannel):
        """Disable a channel from listening to commands."""
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        if str(channel.id) in check_disabled(ctx.guild.id):
            await ctx.send(":x: That channel is already disabled.")
            return
        new_disabled = str(channel.id)
        if check_disabled(ctx.guild.id) != "":
            new_disabled = check_disabled(ctx.guild.id) + f"|{channel.id}"
        cur.execute(
            f'INSERT INTO opts (guildid, disabledchannels, logchannel, modlogchannel, muterole, joinmessage, leavemessage, welcomechannel) VALUES ({ctx.guild.id}, "{channel.id}", NULL, NULL, NULL, NULL, NULL, NULL) ON DUPLICATE KEY UPDATE disabledchannels = "{new_disabled}"')
        db.commit()
        db.close()
        await ctx.send(f":ok_hand: Added **#{channel.name}** ({channel.id}) to the disabled channels for this guild.")

    @commands.command()
    @commands.check(can_manage_guild)
    async def enable(self, ctx, *, channel: discord.TextChannel):
        """Re-enable a previously disabled channel."""
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        if str(channel.id) in check_disabled(ctx.guild.id):
            new_update = check_disabled(ctx.guild.id).replace(str(channel.id) + "|", "").replace("|" + str(channel.id),
                                                                                                 "").replace(
                str(channel.id), "")
            cur.execute(f'UPDATE opts SET disabledchannels = "{new_update}" WHERE guildid = {ctx.guild.id}')
            await ctx.send(
                f":ok_hand: Removed **#{channel.name}** ({channel.id}) from the disabled channels for this guild.")
            db.commit()
            db.close()
        else:
            await ctx.send(":x: That channel is not disabled.")
            db.close()

    @commands.command(aliases=["logsset", "logset"])
    @commands.check(can_manage_guild)
    async def logs(self, ctx, *, channel: discord.TextChannel):
        """Enable the logging feature for a channel."""
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        cur.execute(
            f'INSERT INTO opts (guildid, disabledchannels, logchannel, modlogchannel, muterole, joinmessage, leavemessage, welcomechannel) VALUES ({ctx.guild.id}, NULL, "{channel.id}", NULL, NULL, NULL, NULL, NULL) ON DUPLICATE KEY UPDATE logchannel = "{channel.id}"')
        db.commit()
        db.close()
        await ctx.send(f":ok_hand: Set the logging channel to **#{channel.name}** ({channel.id})")

    @commands.command(aliases=["muteroleset"])
    @commands.check(can_manage_guild)
    async def muterole(self, ctx, *, role: discord.Role):
        """Set the mute role for this guild."""
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        cur.execute(
            f'INSERT INTO opts (guildid, disabledchannels, logchannel, modlogchannel, muterole, joinmessage, leavemessage, welcomechannel) VALUES ({ctx.guild.id}, NULL, NULL, NULL, "{role.id}", NULL, NULL, NULL) ON DUPLICATE KEY UPDATE muterole = "{role.id}"')
        db.commit()
        db.close()
        await ctx.send(f":ok_hand: Set the mute role to **{role.name}** ({role.id})")

    @commands.command(aliases=["modlogset", "modlog"])
    @commands.check(can_manage_guild)
    async def modlogs(self, ctx, *, channel: discord.TextChannel):
        """Enable the mod log feature for this guild."""
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        cur.execute(
            f'INSERT INTO opts (guildid, disabledchannels, logchannel, modlogchannel, muterole, joinmessage, leavemessage, welcomechannel) VALUES ({ctx.guild.id}, NULL, NULL, "{channel.id}", NULL, NULL, NULL) ON DUPLICATE KEY UPDATE modlogchannel = "{channel.id}"')
        db.commit()
        db.close()
        await ctx.send(f":ok_hand: Set the mod log channel to **#{channel.name}** ({channel.id})")

    @commands.command()
    @commands.check(can_manage_guild)
    async def joinmessage(self, ctx, *, message: str):
        """Set the message that Kumiko will send to this guild's set welcome channel on the evnt of a user joining.
        To get a list of available modifiers and how to use them, **click [here](https://github.com/Desiiii/Kumiko/wiki/Modifiers)**"""
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        cur.execute(
            f'INSERT INTO opts (guildid, disabledchannels, logchannel, modlogchannel, muterole, joinmessage, leavemessage, welcomechannel) VALUES ({ctx.guild.id}, NULL, NULL, NULL, NULL, "{message}", NULL, NULL) ON DUPLICATE KEY UPDATE joinmessage = "{message}"')
        db.commit()
        db.close()
        msg = "\N{OK HAND SIGN} Set this guild's join message."
        if not get_welcome_channel(ctx.guild.id) or not self.bot.get_channel(int(get_welcome_channel(ctx.guild.id))):
            msg += "\nNote: I couldn't find a set welcome channel in this guild. You should reset your welcome " \
                   + "channel. Check the wiki if you need help. (<https://github.com/Desiiii/Kumiko/wiki>)"
        await ctx.send(msg)

    @commands.command()
    @commands.check(can_manage_guild)
    async def leavemessage(self, ctx, *, message: str):
        """Set the message that Kumiko will send to this guild's set welcome channel on the event of a user leaving.
        To get a list of available modifiers and how to use them, **click [here](https://github.com/Desiiii/Kumiko/wiki/Modifiers)**"""
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        cur.execute(
            f'INSERT INTO opts (guildid, disabledchannels, logchannel, modlogchannel, muterole, joinmessage, leavemessage, welcomechannel) VALUES ({ctx.guild.id}, NULL, NULL, NULL, NULL, NULL, "{message}", NULL) ON DUPLICATE KEY UPDATE leavemessage = "{message}"')
        db.commit()
        db.close()
        msg = "\N{OK HAND SIGN} Set this guild's leave message."
        if not get_welcome_channel(ctx.guild.id) or not self.bot.get_channel(int(get_welcome_channel(ctx.guild.id))):
            msg += "\nNote: I couldn't find a set welcome channel in this guild. You should reset your welcome " \
                   + "channel. Check the wiki if you need help. (<https://github.com/Desiiii/Kumiko/wiki>)"
        await ctx.send(msg)

    @commands.command(aliases=["welcomechannel", "welcomeset"])
    @commands.check(can_manage_guild)
    async def welcome(self, ctx, *, channel: discord.TextChannel):
        """Enable the welcoming feature."""
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        cur.execute(
            f'INSERT INTO opts (guildid, disabledchannels, logchannel, modlogchannel, muterole, joinmessage, leavemessage, welcomechannel) VALUES ({ctx.guild.id}, NULL, NULL, NULL, NULL, NULL, NULL, "{channel.id}") ON DUPLICATE KEY UPDATE welcomechannel = "{channel.id}"')
        db.commit()
        db.close()
        await ctx.send(f":ok_hand: Set the welcome channel to **#{channel.name}** ({channel.id})")

    @commands.command()
    @commands.check(can_manage_guild)
    async def logtest(self, ctx):
        """Test the logging feature."""
        if get_log_channel(ctx.guild.id):
            c = self.bot.get_channel(int(get_log_channel(ctx.guild.id)))
            try:
                await c.send("```diff\n-Testing\n+Logs```")
                await ctx.send(":ok_hand: Logs successfully sent.")
            except:
                await ctx.send(
                    ":x: An error occurred, check my permissions to make sure I can send messages in the log channel! ({})".format(
                        c.mention))
        else:
            await ctx.send(":x: There doesn't seem to be a logging channel set here :(")

    @commands.command()
    @commands.check(can_manage_guild)
    async def modlogtest(self, ctx):
        """Test out the mod logging feature and check if I have the proper permissions to send messages & embeds in it."""
        if get_modlog_channel(ctx.guild.id):
            c = self.bot.get_channel(int(get_modlog_channel(ctx.guild.id)))
            try:
                await c.send(embed=discord.Embed(
                    description="**Action:** Modlogtest\n"
                                + "**User:** None\n",
                    color=0x00ff00).set_author(
                    name=str(ctx.author),
                    icon_url=ctx.author.avatar_url.replace("?size=1024", ""))
                )
                await ctx.send(":ok_hand: Modlogs successfully tested.")
            except:
                await ctx.send(
                    ":x: An error seems to have occurred, make sure I can send messages and embed links in the modlog channel. ({})".format(
                        c.mention))
        else:
            await ctx.send(":x: There doesn't seem to be a modlog channel set here ;w;")

    @commands.command(name="check")
    async def _check(self, ctx):
        """Check all of the current set options for this guild."""
        disabled = "None"
        if check_disabled(ctx.guild.id):
            list = check_disabled(ctx.guild.id).split('|')
            disabled = ", ".join([self.bot.get_channel(int(l)).mention for l in list])
        logchannel = "None"
        if get_log_channel(ctx.guild.id):
            logchannel = self.bot.get_channel(int(get_log_channel(ctx.guild.id))).mention
        modlog = "None"
        if get_modlog_channel(ctx.guild.id):
            modlog = self.bot.get_channel(int(get_modlog_channel(ctx.guild.id))).mention
        welcome = "None"
        if get_welcome_channel(ctx.guild.id):
            welcome = self.bot.get_channel(int(get_welcome_channel(ctx.guild.id))).mention
        joinmsg = "None"
        if get_join_message(ctx.guild.id):
            joinmsg = get_join_message(ctx.guild.id)
        leavemsg = "None"
        if get_leave_message(ctx.guild.id):
            leavemsg = get_leave_message(ctx.guild.id)
        muterole = "None"
        if get_mute_role(ctx.guild.id):
            role = discord.utils.get(ctx.guild.roles, id=int(get_mute_role(ctx.guild.id)))
            muterole = role.name if role is not None else "Role was deleted"
        await ctx.send(f"**{ctx.guild.name}**'s Options\n"
                       + f"**Disabled Channels:** {disabled}\n"
                       + f"**Logging Channel:** {logchannel}\n"
                       + f"**ModLog Channel:** {modlog}\n"
                       + f"**Welcome Channel:** {welcome}\n"
                       + f"**Join Message:** {joinmsg}\n"
                       + f"**Leave Message:** {leavemsg}\n"
                       + f"**Mute Role:** {muterole}")


def setup(bot):
    bot.add_cog(Options(bot))
