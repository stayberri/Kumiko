from discord.ext import commands
import json
from os import path

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "..", "..", "config.json"))
with open(filepath, 'r') as f:
    config = json.load(f)

ownerids = config['owners']


def is_dev(ctx):
    return ctx.author.id in ownerids


def can_ban(ctx):
    return ctx.author.id in ownerids or ctx.author.guild_permissions.ban_members


def can_kick(ctx):
    return ctx.author.id in ownerids or ctx.author.guild_permissions.kick_members


def can_manage_guild(ctx):
    return ctx.author.id in ownerids or ctx.author.guild_permissions.manage_guild


def can_manage_messages(ctx):
    return ctx.author.id in ownerids or ctx.author.guild_permissions.manage_messages
