import discord
import json
from discord.ext import commands
from cogs.utils.logger import *

with open('config.json', 'r') as f:
    config = json.load(f)
bot = commands.Bot(command_prefix=config['prefix'])

startup_extensions = ["cogs.owner", "cogs.fun", "cogs.info", "cogs.mod"]


@bot.event
async def on_ready():
    global console
    console = bot.get_channel(388807365400461332)
    await send_log_event(console, "[Kumiko][Logger]\n"
                         + "Starting up bot account:\n"
                         + str(bot.user) + "\n"
                         + f"Loaded up {len(bot.commands)} commands for {len(bot.guilds)} guilds.")
    await bot.change_presence(game=discord.Game(name="kumiko help | Lars is cute"))


@bot.event
async def on_message(message):
    if not message.author.bot:
        await bot.process_commands(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            f":x: U-uh, sorry! You probably missed a required argument! Check `{ctx.prefix}help {ctx.command}`")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send(":x: You do not have the permission required for this command.")
    elif isinstance(error, commands.UserInputError):
        await ctx.send(f":x: The input you gave me caused an error! Make sure to check `{ctx.prefix}help {ctx.command}`")
    elif isinstance(error, commands.CommandNotFound):
        pass
    else:
        await ctx.send(f":x: {str(error)}")
        await send_log_event(console, f"I ran into an error on command `{ctx.command}`:\n{str(error)}")


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

bot.run(config['token'])