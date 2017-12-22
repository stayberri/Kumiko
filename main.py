import discord, itertools, inspect, re
import json
import aiohttp
import traceback
from discord.ext import commands
from cogs.utils.logger import *
from cogs.utils.tools import *

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
        if not message.author.bot:
            await self.process_commands(message)
            if message.content == "<@!315297886613012481>" or message.content == "<@315297886613012481>":
                await message.channel.send(":wave: Hi! My prefixes are `k.`, `kumiko`, and `@Kumiko#0304`. Use them like\n"
                                           + "`k.help`\n`kumiko help`\n`@Kumiko#0304 help`")
    async def on_guild_join(self, guild):
        await send_log_event(console, f":tada: I joined the guild `{guild.name}` with `{len(guild.members)}` members owned by `{guild.owner}`")

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(":x: You do not have the permission required for this command.")
        elif isinstance(error, commands.UserInputError) or isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(":x: Y-You provided improper arguments or didn't give me any. Check the command help below!",
                           embed=get_embedded_help_for(ctx.command, ctx))
            ctx.command.reset_cooldown(ctx)
        elif isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            await ctx.send(f':x: You can use this command again in {"%d hours, %02d minutes and %02d seconds" % (h, m, s)}')
        elif isinstance(error, commands.CommandNotFound):
            pass
        else:
            await ctx.send(f":x: {str(error)}")
            await send_log_event(console, f"I ran into an error on command `{ctx.command}`:\n{str(error)}")

KumikoBot().run(config['token'])