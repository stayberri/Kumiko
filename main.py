import discord, itertools, inspect, re
import json
import aiohttp
import traceback
import pymysql
import pytz
from discord.ext import commands
from cogs.utils.logger import *
from cogs.utils.tools import *
from cogs.utils.db import *

with open('config.json', 'r') as f:
    config = json.load(f)

desc = """
Kumiko: A discord bot dedicated for moderation, information, and fun.
"""

initial_extensions = (
    "cogs.owner",
    "cogs.fun",
    "cogs.info",
    "cogs.mod",
    "cogs.action",
    "cogs.image",
    "cogs.currency",
    "cogs.opts",
    "cogs.logs",
)


class KumikoBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=config['prefix'], description=desc)

        self.console = 388807365400461332
        self.remove_command("help")

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}.')
                print(traceback.format_exc())

    async def on_ready(self):
        global console
        console = self.get_channel(self.console)
        await send_log_event(console, "[Kumiko][Logger]\n"
                             + "Starting up bot account:\n"
                             + str(self.user) + "\n"
                             + f"Loaded up {len(self.commands)} commands for {len(self.guilds)} guilds.")
        await self.change_presence(game=discord.Game(name="kumiko help | Lars is cute"))

    async def on_resumed(self):
        await send_log_event(console, "[Kumiko][Logger]\n"
                             + "Somehow lost connection to Discord (??) and successfully resumed.")

    async def on_message(self, message):
        if not message.author.bot and message.guild is not None:
            if not str(message.channel.id) in check_disabled(message.guild.id):
                await self.process_commands(message)
                if message.content == "<@!315297886613012481>" or message.content == "<@315297886613012481>":
                    await message.channel.send(":wave: Hi! My prefixes are `k.`, `kumiko`, and `@Kumiko#0304`. Use them like\n"
                                               + "`k.help`\n`kumiko help`\n`@Kumiko#0304 help`")

    async def on_guild_join(self, guild):
        await send_log_event(console, f":tada: I joined the guild `{guild.name}` with `{len(guild.members)}` members owned by `{guild.owner}`")
        await post_guild_count(len(self.guilds), self.user.id)
        await send_log_event(console, "\N{OK HAND SIGN} Posted guild count to DBL")

    async def on_guild_remove(self, guild):
        await send_log_event(console, f":sob: I left the guild `{guild.name}` with `{len(guild.members)}` members owned by `{guild.owner}`")
        await post_guild_count(len(self.guilds), self.user.id)
        await send_log_event(console, "\N{OK HAND SIGN} Posted guild count to DBL")

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(":x: You do not have the permission required for this command.")
        elif isinstance(error, commands.UserInputError) or isinstance(error, commands.MissingRequiredArgument):
            db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'], charset='utf8mb4')
            cur = db.cursor()
            if str(ctx.command) == "logs" and "reset" in ctx.message.content:
                cur.execute(f'INSERT INTO opts (guildid, disabledchannels, logchannel, modlogchannel, muterole, joinmessage, leavemessage, welcomechannel) VALUES ({ctx.guild.id}, NULL, NULL, NULL, NULL, NULL, NULL, NULL) ON DUPLICATE KEY UPDATE logchannel = NULL')
                db.commit()
                db.close()
                await ctx.send(":ok_hand: Reset the log channel.")
                return
            elif str(ctx.command) == "muterole" and "reset" in ctx.message.content:
                cur.execute(f'INSERT INTO opts (guildid, disabledchannels, logchannel, modlogchannel, muterole, joinmessage, leavemessage, welcomechannel) VALUES ({ctx.guild.id}, NULL, NULL, NULL, NULL, NULL, NULL, NULL) ON DUPLICATE KEY UPDATE muterole = NULL')
                db.commit()
                db.close()
                await ctx.send(":ok_hand: Reset the mute role.")
                return
            elif str(ctx.command) == "joinmessage" and "reset" in ctx.message.content:
                cur.execute(
                    f'INSERT INTO opts (guildid, disabledchannels, logchannel, modlogchannel, muterole, joinmessage, leavemessage, welcomechannel) VALUES ({ctx.guild.id}, NULL, NULL, NULL, NULL, NULL, NULL, NULL) ON DUPLICATE KEY UPDATE joinmessage = NULL')
                db.commit()
                db.close()
                await ctx.send(":ok_hand: Reset the join message.")
                return
            elif str(ctx.command) == "leavemessage" and "reset" in ctx.message.content:
                cur.execute(f'INSERT INTO opts (guildid, disabledchannels, logchannel, modlogchannel, muterole, joinmessage, leavemessage, welcomechannel) VALUES ({ctx.guild.id}, NULL, NULL, NULL, NULL, NULL, NULL, NULL) ON DUPLICATE KEY UPDATE leavemessage = NULL')
                db.commit()
                db.close()
                await ctx.send(":ok_hand: Reset the leave message.")
                return
            elif str(ctx.command) == "welcome" and "reset" in ctx.message.content:
                cur.execute(f'INSERT INTO opts (guildid, disabledchannels, logchannel, modlogchannel, muterole, joinmessage, leavemessage, welcomechannel) VALUES ({ctx.guild.id}, NULL, NULL, NULL, NULL, NULL, NULL, NULL) ON DUPLICATE KEY UPDATE leavemessage = NULL')
                db.commit()
                db.close()
                await ctx.send(":ok_hand: Reset the welcome channel.")
                return
            await ctx.send(":x: Y-You provided improper arguments or didn't give me any. Check the command help below!",
                           embed=get_embedded_help_for(ctx.command, ctx))
            ctx.command.reset_cooldown(ctx)
            db.close()
        elif isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            await ctx.send(f':x: You can use this command again in {"%d hours, %02d minutes and %02d seconds" % (h, m, s)}' + (" (about now)." if error.retry_after == 0 else "."))
        elif isinstance(error, commands.CommandNotFound):
            pass
        else:
            await ctx.send(f":x: {str(error)}")
            await send_log_event(console, f"I ran into an error on command `{ctx.command}`:\n{str(error)}")

KumikoBot().run(config['token'])