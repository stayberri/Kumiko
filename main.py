import discord
import json
import aiohttp
import traceback
from discord.ext import commands
from cogs.utils.logger import *

with open('config.json', 'r') as f:
    config = json.load(f)

initial_extensions = (
    "cogs.owner",
    "cogs.fun",
    "cogs.info",
    "cogs.mod",
)


class KumikoBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=config['prefix'])

        self.console = 388807365400461332

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

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f":x: U-uh, sorry! You probably missed a required argument! Check `{ctx.prefix}help {ctx.command}`")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(":x: You do not have the permission required for this command.")
        elif isinstance(error, commands.UserInputError):
            await ctx.send(
                f":x: The input you gave me caused an error! Make sure to check `{ctx.prefix}help {ctx.command}`")
        elif isinstance(error, commands.CommandNotFound):
            pass
        else:
            await ctx.send(f":x: {str(error)}")
            await send_log_event(console, f"I ran into an error on command `{ctx.command}`:\n{str(error)}")

KumikoBot().run(config['token'])