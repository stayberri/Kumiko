import discord
import traceback
from discord.ext import commands

from .utils.checks import *
from .utils.db import *


class Mod:
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
            mod_log_id = get_modlog_channel(ctx.guild.id)
            if mod_log_id:
                mod_log = self.bot.get_channel(int(mod_log_id))
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
    async def softban(self, ctx, member: discord.Member, *, reason: str = None):
        """Ban a member from the guild.
        You can also supply an optional reason. This will also send a message to the set modlog channel"""
        r = reason
        if not reason:
            r = "No reason given."
        if ctx.author.top_role.position > member.top_role.position:
            try:
                await ctx.guild.ban(member, reason=r)
                await ctx.guild.unban(member)
            except discord.Forbidden:
                await ctx.send(
                    f":x: I-I'm sorry, I couldn't ban `{member}` because I either don't have ban permissions "
                    + "or my role is lower than theirs.")
                return
            mod_log_id = get_modlog_channel(ctx.guild.id)
            if mod_log_id:
                mod_log = self.bot.get_channel(int(mod_log_id))
                if mod_log.permissions_for(ctx.guild.me).send_messages:
                    await mod_log.send(embed=discord.Embed(
                        description="**Action:** SoftBan\n"
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
    @commands.check(can_kick)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None):
        """Kick a member from the guild.
        You can also supply an optional reason. This will also send a message to the set modlog channel"""
        r = reason
        if not reason:
            r = "No reason given."
        if ctx.author.top_role.position > member.top_role.position:
            try:
                await ctx.guild.kick(member, reason=r)
            except discord.Forbidden:
                await ctx.send(
                    f":x: I-I'm sorry, I couldn't kick `{member}` because I either don't have kick permissions "
                    + "or my role is lower than theirs.")
                return
            mod_log_id = get_modlog_channel(ctx.guild.id)
            if mod_log_id:
                mod_log = self.bot.get_channel(int(mod_log_id))
                if mod_log.permissions_for(ctx.guild.me).send_messages:
                    await mod_log.send(embed=discord.Embed(
                        description="**Action:** Kick\n"
                                    + "**User:** " + str(member) + "\n"
                                    + "**Reason:** " + r,
                        color=0xff0000).set_author(
                        name=str(ctx.author),
                        icon_url=ctx.author.avatar_url.replace("?size=1024", ""))
                    )
            await ctx.send(f":ok_hand: I kicked **{member}** for `{r}`")
        else:
            await ctx.send(":x: I-I'm sorry, but you can't ban someone with a higher role than you!")

    @commands.command()
    @commands.check(can_ban)
    async def hackban(self, ctx, user_id: int, *, reason: str = None):
        """Ban a member by their user ID.
        You can also supply an optional reason. This will also send a message to the set modlog channel."""
        member = await self.bot.get_user_info(user_id)
        r = reason
        if not reason:
            r = "No reason given."
        if member.id in [m.id for m in ctx.guild.members] and ctx.author.top_role.position > discord.utils.get(
                ctx.guild.members, id=member.id).top_role.position or member not in ctx.guild.members:
            try:
                await ctx.guild.ban(member, reason=r)
            except discord.Forbidden:
                await ctx.send(
                    f":x: I-I'm sorry, I couldn't ban `{member}` because I either don't have ban permissions "
                    + "or my role is lower than theirs.")
                return
            mod_log_id = get_modlog_channel(ctx.guild.id)
            if mod_log_id:
                mod_log = self.bot.get_channel(int(mod_log_id))
                if mod_log and mod_log.permissions_for(ctx.guild.me).send_messages:
                    await mod_log.send(embed=discord.Embed(
                        description="**Action:** Hackban\n"
                                    + "**User:** " + str(member) + "\n"
                                    + "**Reason:** " + r,
                        color=0xff0000).set_author(
                        name=str(ctx.author),
                        icon_url=ctx.author.avatar_url.replace("?size=1024", ""))
                    )
            await ctx.send(f":ok_hand: I banned **{member}** for `{r}` successfully.")
        else:
            await ctx.send(":x: I-I'm sorry, but you can't ban someone with a higher role than you!")

    @commands.command()
    @commands.check(can_ban)
    async def unban(self, ctx, user_id: int):
        """This command allows you to unban a user by their ID."""
        if user_id not in [u.user.id for u in await ctx.guild.bans()]:
            await ctx.send(":x: U-uh, excuse me! That user doesn't seem to be banned!")
            return
        user = await self.bot.get_user_info(user_id)
        try:
            await ctx.guild.unban(user)
        except discord.Forbidden:
            await ctx.send(
                ":x: Aaaaaa I-I'm sorry, I couldn't unban the person because I don't have the proper permissions")
            return
        mod_log_id = get_modlog_channel(ctx.guild.id)
        if mod_log_id:
            mod_log = self.bot.get_channel(int(mod_log_id))
            if mod_log and mod_log.permissions_for(ctx.guild.me).send_messages:
                await mod_log.send(embed=discord.Embed(
                    description="**Action:** Unban\n"
                                + "**User:** " + str(user) + "\n",
                    color=0x00ff00).set_author(
                    name=str(ctx.author),
                    icon_url=ctx.author.avatar_url.replace("?size=1024", ""))
                )
        await ctx.send(
            f":ok_hand: I unbanned **{user}** successfully")

    @commands.command()
    @commands.check(can_manage_messages)
    async def prune(self, ctx, *, number_of_messages: int):
        """Prune a number of messages from a channel.
        Minimum is 3, maximum is 100. If the number is > 100, it will shrink down to 100 for you"""
        if number_of_messages > 100:
            number_of_messages = 100
        if number_of_messages < 3:
            await ctx.send(":x: B-baka! That's too few messages!")
            return
        mgs = []
        async for m in ctx.channel.history(limit=number_of_messages):
            mgs.append(m)
        await ctx.channel.delete_messages(mgs)
        await ctx.send(f":white_check_mark: Deleted `{len(mgs)}` messages!", delete_after=5)

    @commands.command()
    @commands.check(can_ban)
    async def mute(self, ctx, user: discord.Member, *, reason: str = None):
        """Mute a user.
        This relies on the idea that you have set a mute role using the `muterole` command."""
        if reason is None:
            reason = "No reason given."
        if ctx.author.top_role.position > user.top_role.position:
            if get_mute_role(ctx.guild.id):
                mute_role = discord.utils.get(ctx.guild.roles, id=int(get_mute_role(ctx.guild.id)))
                if mute_role:
                    if mute_role not in user.roles:
                        try:
                            await user.add_roles(mute_role, reason=reason)
                        except:
                            await ctx.send(
                                ":x: I-I'm sorry, I ran into an error. Make sure I can manage roles and that my highest"
                                + " role is above this guild's set mute role! ({})".format(
                                    mute_role.name))
                            return
                        mod_log_id = get_modlog_channel(ctx.guild.id)
                        if mod_log_id:
                            mod_log = self.bot.get_channel(int(mod_log_id))
                            if mod_log and mod_log.permissions_for(ctx.guild.me).send_messages:
                                await mod_log.send(embed=discord.Embed(
                                    description="**Action:** Mute\n"
                                                + "**User:** " + str(user) + "\n"
                                                + "**Reason:** " + reason,
                                    color=0xff0000).set_author(
                                    name=str(ctx.author),
                                    icon_url=ctx.author.avatar_url.replace("?size=1024", ""))
                                )
                        await ctx.send(f":ok_hand: Muted **{user}** with success.")
                    else:
                        await ctx.send(":x: That user is already muted.")
                else:
                    await ctx.send(
                        ":x: The set mute role in this guild seems to have been deleted. Reset the mute role and try again.")
            else:
                await ctx.send(
                    ":x: I-I'm sorry, you can't mute a user when there is no mute role set! set it using `{}muterole <role>`".format(
                        ctx.prefix))
        else:
            await ctx.send(":x: You can't mute users who are in a higher role than you!")

    @commands.command()
    @commands.check(can_ban)
    async def unmute(self, ctx, user: discord.Member):
        """Unmute a user."""
        if ctx.author.top_role.position > user.top_role.position:
            if get_mute_role(ctx.guild.id):
                mute_role = discord.utils.get(ctx.guild.roles, id=int(get_mute_role(ctx.guild.id)))
                if mute_role:
                    if mute_role in user.roles:
                        try:
                            await user.remove_roles(mute_role)
                        except:
                            await ctx.send(
                                ":x: I-I'm sorry, I ran into an error. Make sure I can manage roles and that my highest role is above this guild's set mute role! ({})".format(
                                    mute_role.name))
                            return
                        mod_log_id = get_modlog_channel(ctx.guild.id)
                        if mod_log_id:
                            mod_log = self.bot.get_channel(int(mod_log_id))
                            if mod_log and mod_log.permissions_for(ctx.guild.me).send_messages:
                                await mod_log.send(embed=discord.Embed(
                                    description="**Action:** Unmute\n"
                                                + "**User:** " + str(user) + "\n",
                                    color=0x00ff00).set_author(
                                    name=str(ctx.author),
                                    icon_url=ctx.author.avatar_url.replace("?size=1024", ""))
                                )
                        await ctx.send(f":ok_hand: Unmuted **{user}** with success.")
                    else:
                        await ctx.send(":x: That user is not muted")
                else:
                    await ctx.send(
                        ":x: The set mute role in this guild seems to have been deleted. Reset the mute role and try again.")
            else:
                await ctx.send(
                    ":x: I-I'm sorry, you can't mute a user when there is no mute role set! set it using `{}muterole <role>`".format(
                        ctx.prefix))
        else:
            await ctx.send(":x: You can't mute users who are in a higher role than you!")

    @commands.command()
    @commands.check(can_manage_roles)
    async def role(self, ctx, user: discord.Member, *, role: discord.Role):
        """Apply or remove a role from a user.
        If you are searching with username/nickname, you must surround the user in quotations ("). The role field should not have this unless the role name has it."""
        if role.position >= ctx.author.top_role.position:
            await ctx.send(":x: You can't manage roles higher than your highest role.")
        elif role.position >= ctx.me.top_role.position:
            await ctx.send(":x: I can't manage that role.")
        else:
            if role not in user.roles:
                try:
                    await user.add_roles(role)
                except discord.Forbidden:
                    await ctx.send(":x: I don't seem to have the permission to manage roles.")
                    return
                await ctx.send(f":ok_hand: Added the {role.name} role to {user.display_name}")
            else:
                try:
                    await user.remove_roles(role)
                except discord.Forbidden:
                    await ctx.send(":x: I don't seem to have the permission to manage roles.")
                    return
                await ctx.send(f":ok_hand: Removed the {role.name} role from {user.display_name}")


def setup(bot):
    bot.add_cog(Mod(bot))
