import discord
client = discord.Client()

async def send_log_event(console, msg):
    print(msg)
    await console.send(msg)