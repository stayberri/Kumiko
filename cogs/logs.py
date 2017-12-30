import discord
import pytz
from discord.ext import commands
from .utils.tools import *
from .utils.db import *


class GuildLogs:
    def __init__(self, bot):
        self.bot = bot

    async def on_message_edit(self, before, after):
        bmsg = before.clean_content
        bmsg = bmsg.replace("```", "")
        amsg = after.clean_content
        amsg = amsg.replace("```", "")
        logid = get_log_channel(int(before.guild.id))
        if logid:
            logs = self.bot.get_channel(int(logid))
            if amsg == "" or bmsg == "" or after.channel.id == logs.id or amsg == bmsg:
                return
            await logs.send(':tools: [`' + str(datetime.datetime.now(pytz.timezone('America/New_York')).strftime(
                "%H:%M:%S")) + '`] Message by **{0}** in {1} was edited. ```diff\n-{2}\n+{3}\n```'.format(
                str(after.author), after.channel.mention, bmsg, amsg))

    async def on_guild_emojis_update(self, before, after):
        try:
            logid = get_log_channel(int(after[0].guild.id))
        except IndexError:
            logid = get_log_channel(int(before[0].guild.id))
        if logid:
            logs = self.bot.get_channel(int(logid))
            afterEmojis = sorted(after, key=lambda x: x.id)
            beforeEmojis = sorted(before, key=lambda x: x.id)
            for ae in afterEmojis:
                if ae not in beforeEmojis:
                    await logs.send(":white_check_mark: [`" + str(
                        datetime.datetime.now(pytz.timezone('America/New_York')).strftime(
                            "%H:%M:%S")) + "`] Emoji `{0}` added: {1}".format(ae.name, str(ae)))
            for be in beforeEmojis:
                if be not in afterEmojis:
                    await logs.send(":x: [`" + str(datetime.datetime.now(pytz.timezone('America/New_York')).strftime("%H:%M:%S")) + "`] Emoji `{}` deleted.".format(be.name))
            if len(beforeEmojis) == len(afterEmojis):
                for i in range(0, len(afterEmojis)):
                    if beforeEmojis[i].name != afterEmojis[i].name:
                        await logs.send(":pencil: [`" + str(datetime.datetime.now(pytz.timezone('America/New_York')).strftime(
                            "%H:%M:%S")) + "`] Name of emoji `{0}` updated to `{1}`: {2}".format(beforeEmojis[i].name,
                                                                                                 afterEmojis[i].name,
                                                                                                 str(afterEmojis[i])))

    async def on_message_delete(self, message):
        msg = message.clean_content
        msg = msg.replace("```", "")
        logid = get_log_channel(int(message.guild.id))
        if logid:
            logs = self.bot.get_channel(int(logid))
            if msg == "":
                abc = 123
                return
            if message.channel.id == logs.id:
                cba = 321
                return
            await logs.send(':x: [`' + str(datetime.datetime.now(pytz.timezone('America/New_York')).strftime("%H:%M:%S")) + '`] Message by **' + str(message.author) + '** in ' + message.channel.mention + ' was deleted. ```diff\n-' + msg + '```')

    async def on_guild_channel_create(self, channel):
        logid = get_log_channel(int(channel.guild.id))
        if logid:
            logs = self.bot.get_channel(int(logid))
            if isinstance(channel, discord.TextChannel):
                type = "text"
            elif isinstance(channel, discord.VoiceChannel):
                type = "voice"
            else:
                type = "category"
            await logs.send(":white_check_mark: [`" + str(datetime.datetime.now(pytz.timezone('America/New_York')).strftime(
                "%H:%M:%S")) + "`] New channel was created. ```diff\n+Name: {0}\n+Topic: {1}\n+ID: {2}\n+Type: {3}\n```".format(
                channel.name, channel.topic, channel.id, type))

    async def on_guild_channel_delete(self, channel):
        logid = get_log_channel(int(channel.guild.id))
        if logid:
            logs = self.bot.get_channel(int(logid))
            await logs.send(":x: [`" + str(datetime.datetime.now(pytz.timezone('America/New_York')).strftime(
                "%H:%M:%S")) + "`] Channel was deleted. ```diff\n-Name: {0}\n-ID: {1}\n-Type: {2}\n```".format(
                channel.name, channel.id, channel.type))

    async def on_guild_channel_update(self, before, after):
        logid = get_log_channel(int(before.guild.id))
        if logid:
            logs = self.bot.get_channel(int(logid))
            if isinstance(before, discord.TextChannel) and after.topic != before.topic:
                await logs.send(":tools: [`" + str(datetime.datetime.now(pytz.timezone('America/New_York')).strftime("%H:%M:%S")) + "`] Channel {0} was edited. ```diff\n-Topic: {1}\n+Topic: {2}\n```".format(after.mention, before.topic, after.topic))
            if after.name != before.name:
                await logs.send(":tools: [`" + str(datetime.datetime.now(pytz.timezone('America/New_York')).strftime("%H:%M:%S")) + "`] Channel {0} was edited. ```diff\n-Name: {1}\n+Name: {2}\n```".format(after.mention, before.name, after.name))

    async def on_member_update(self, before, after):
        logid = get_log_channel(int(before.guild.id))
        if logid:
            logs = self.bot.get_channel(int(logid))
            if after.display_name != before.display_name:
                if after.display_name != after.name and before.display_name != before.name:
                    await logs.send(":tools: [`" + str(datetime.datetime.now(pytz.timezone('America/New_York')).strftime("%H:%M:%S")) + "`] Nickname of **{0}** was changed. ```diff\n-{1}\n+{2}\n```".format(str(after),before.display_name,after.display_name))
            if after.name != before.name:
                await logs.send(":tools: [`" + str(datetime.datetime.now(pytz.timezone('America/New_York')).strftime("%H:%M:%S")) + "`] Username of **{0}** was changed. ```diff\n-{1}\n+{2}\n```".format(str(after), before.name, after.name))
            if after.roles != before.roles:
                beforeRoles = ""
                afterRoles = ""
                beforeSorted = sorted(before.roles, key=lambda x: -x.position)
                afterSorted = sorted(after.roles, key=lambda x: -x.position)
                for role in beforeSorted:
                    beforeRoles += role.name + ", "
                beforeRoles = beforeRoles.replace(", @everyone, ", "")
                beforeRoles = beforeRoles.replace("@everyone, ", "")
                for role in afterSorted:
                    afterRoles += role.name + ", "
                afterRoles = afterRoles.replace(", @everyone, ", "")
                afterRoles = afterRoles.replace("@everyone, ", "")
                if str(afterRoles) == str(beforeRoles):
                    print("Weird exception??")
                    return
                await logs.send(":tools: [`" + str(datetime.datetime.now(pytz.timezone('America/New_York')).strftime("%H:%M:%S")) + "`] Roles from **{0}** updated.".format(str(after)) + "\n```diff\n-" + beforeRoles + "\n+" + afterRoles + "\n```")

    async def on_member_join(self, member):
        logid = get_log_channel(int(member.guild.id))
        welcomeid = get_welcome_channel(int(member.guild.id))
        if logid:
            logs = self.bot.get_channel(int(logid))
            await logs.send(":mega: [`" + str(datetime.datetime.now(pytz.timezone('America/New_York')).strftime("%H:%M:%S")) + "`] `{0}` joined `{1}`. (`User ID: {2}`)".format(str(member), member.guild.name, member.id))
        if welcomeid:
            if get_join_message(member.guild.id):
                welcome = self.bot.get_channel(int(welcomeid))
                joinmsg = parse_modifiers(get_join_message(member.guild.id), member, member.guild)
                await welcome.send(joinmsg)

    async def on_member_remove(self, member):
        logid = get_log_channel(int(member.guild.id))
        welcomeid = get_welcome_channel(int(member.guild.id))
        if logid:
            logs = self.bot.get_channel(int(logid))
            await logs.send(":mega: [`" + str(datetime.datetime.now(pytz.timezone('America/New_York')).strftime("%H:%M:%S")) + "`] `{0}` left `{1}`. (`User ID: {2}`)".format(str(member), member.guild.name, member.id))
        if welcomeid:
            if get_leave_message(member.guild.id):
                welcome = self.bot.get_channel(int(welcomeid))
                leavemsg = parse_modifiers(get_leave_message(member.guild.id), member, member.guild)
                await welcome.send(leavemsg)

    async def on_guild_role_create(self, role):
        logid = get_log_channel(int(role.guild.id))
        if logid:
            logs = self.bot.get_channel(int(logid))
            await logs.send(":white_check_mark: New role created. ```diff\n"
                            + f"+Name: {role.name}\n"
                            + f"+ID: {role.id}\n"
                            + f"+Colour: {role.color}\n"
                            + f"+Permissions: {role.permissions.value}\n```")

    async def on_guild_role_delete(self, role):
        logid = get_log_channel(int(role.guild.id))
        if logid:
            try:
                logs = self.bot.get_channel(int(logid))
                await logs.send(":x: Role deleted. ```diff\n-Name: {0}\n-ID: {1}\n```".format(role.name, role.id))
            except:
                pass

    async def on_guild_role_update(self, before, after):
        logid = get_log_channel(int(before.guild.id))
        if logid:
            logs = self.bot.get_channel(int(logid))
            if before.name != after.name:
                await logs.send(":tools: Role **{0}** updated. ```diff\n-Name: {1}\n+Name: {2}\n```".format(after.name, before.name, after.name))
            if before.color != after.color:
                await logs.send(":tools: Role **{0}** updated. ```diff\n-Colour: {1}\n+Colour: {2}\n```".format(after.name, before.color, after.color))
            if before.permissions.value != after.permissions.value:
                await logs.send(":tools: Role **{0}** updated. ```diff\n-Permissions: {1}\n+Permissions: {2}\n```".format(after.name, before.permissions.value,after.permissions.value))


def setup(bot):
    bot.add_cog(GuildLogs(bot))