from discord.ext import commands

ownerids = [
    267207628965281792
]


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
