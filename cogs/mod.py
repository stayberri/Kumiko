import discord
from discord.ext import commands

from cogs.utils.checks import *


class Mod():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(can_ban)
    async def ban(self, ctx, member: discord.Member, *, reason: str = None):
        """Ban a member from the guild.
        You can also supply an optional reason. This will also send a message to a #mod-log if it exists."""
        r = reason
        if not reason:
            r = "No reason given."
        if ctx.author.top_role.position > member.top_role.position:
            try:
                await ctx.guild.ban(member, reason=r)
            except discord.Forbidden:
                await ctx.send(
                    f":x: I-I'm sorry, I couldn't ban `{member}` because I either don't have ban permissions "
                    + "or my role is lower than theirs.")
                return
            mod_log = discord.utils.get(ctx.guild.channels, name="mod-log")
            if mod_log and mod_log.permissions_for(ctx.guild.me).send_messages:
                await mod_log.send(embed=discord.Embed(
                    description="**Action:** Ban\n"
                                + "**User:** " + str(member) + "\n"
                                + "**Reason:** " + r,
                    color=0xff0000).set_author(
                    name=str(ctx.author),
                    icon_url=ctx.author.avatar_url.replace("?size=1024", ""))
                )
            await ctx.send(f":ok_hand: I banned **{member}** for `{r}` and I sent a message to #mod-log if it exists")
        else:
            await ctx.send(":x: I-I'm sorry, but you can't ban someone with a higher role than you!")

    @commands.command()
    @commands.check(can_ban)
    async def hackban(self, ctx, user_id: int, *, reason: str = None):
        """Ban a member by their user ID.
        You can also supply an optional reason. This will also send a message to a #mod-log if it exists."""
        member = await self.bot.get_user_info(user_id)
        r = reason
        if not reason:
            r = "No reason given."
        if member.id in [m.id for m in ctx.guild.members] and ctx.author.top_role.position > discord.utils.get(ctx.guild.members, id=member.id).top_role.position or member not in ctx.guild.members:
            try:
                await ctx.guild.ban(member, reason=r)
            except discord.Forbidden:
                await ctx.send(
                    f":x: I-I'm sorry, I couldn't ban `{member}` because I either don't have ban permissions "
                    + "or my role is lower than theirs.")
                return
            mod_log = discord.utils.get(ctx.guild.channels, name="mod-log")
            if mod_log and mod_log.permissions_for(ctx.guild.me).send_messages:
                await mod_log.send(embed=discord.Embed(
                    description="**Action:** Hackban\n"
                                + "**User:** " + str(member) + "\n"
                                + "**Reason:** " + r,
                    color=0xff0000).set_author(
                    name=str(ctx.author),
                    icon_url=ctx.author.avatar_url.replace("?size=1024", ""))
                )
            await ctx.send(f":ok_hand: I banned **{member}** for `{r}` and I sent a message to #mod-log if it exists")
        else:
            await ctx.send(":x: I-I'm sorry, but you can't ban someone with a higher role than you!")

    @commands.command()
    @commands.check(can_ban)
    async def unban(self, ctx, user_id: int):
        """This command allows you to unban a user by their ID."""
        bans = await ctx.guild.bans()
        if user_id not in [u.user.id for u in bans]:
            await ctx.send(":x: U-uh, excuse me! That user doesn't seem to be banned!")
            return



def setup(bot):
    bot.add_cog(Mod(bot))
