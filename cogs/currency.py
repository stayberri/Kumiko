import pymysql
import discord
import json
import random
import traceback
import requests
import asyncio
from discord.ext import commands
from .utils.tools import *
from .utils.db import *

with open('config.json', 'r') as f:
    config = json.load(f)


class Currency:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=1, per=300, type=commands.BucketType.user)
    async def loot(self, ctx):
        """Loot the current channel!
        You can get a maximum of 100 credits. You might also recieve none."""
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        value = random.randint(0, 100)
        cur.execute(
            f'INSERT INTO profiles (userid, description, bal, marryid, reps) VALUES ({ctx.author.id}, NULL, {value}, NULL, 0) ON DUPLICATE KEY UPDATE bal = bal + {value}')
        db.commit()
        if value == 0:
            await ctx.send(":tada: Congratulations, you looted- oh, I-I'm sorry. You didn't loot any credits!")
            db.close()
            return
        await ctx.send(":tada: You looted **{}** credits!".format(value))
        db.close()

    @commands.command(aliases=["bal"])
    async def balance(self, ctx, *, user: discord.Member = None):
        """Check your current balance"""
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        if user is None:
            user = ctx.author
        await ctx.send(f":gem: **{user.display_name}** has a balance of **${get_balance(user.id)}**")
        db.close()

    @commands.command()
    @commands.cooldown(rate=1, per=86400, type=commands.BucketType.user)
    async def daily(self, ctx):
        """Recieve your daily reward."""
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        cur.execute(
            f'INSERT INTO profiles (userid, description, bal, marryid, reps) VALUES ({ctx.author.id}, NULL, 150, NULL, 0) ON DUPLICATE KEY UPDATE bal = bal + 150')
        db.commit()
        await ctx.send(":white_check_mark: You successfully claimed your daily credits of **$150**")
        db.close()

    @commands.command()
    async def profile(self, ctx, *, user: discord.Member = None):
        """Check your profile or the profile of another user."""
        if user is None:
            user = ctx.author
        if user.bot:
            await ctx.send(":x: Bots don't have profiles.")
            return
        if get_married(user.id):
            m = await self.bot.get_user_info(get_married(user.id))
        else:
            m = "Nobody"
        em = discord.Embed(
            title=user.display_name + "'s profile",
            description=get_description(user.id),
            color=ctx.author.color
        ).add_field(
            name="💰 Balance",
            value=get_balance(user.id)
        ).add_field(
            name="💜 Married With",
            value=m
        ).add_field(
            name="🏅 Reputation",
            value=get_reps(user.id)
        ).set_thumbnail(
            url=user.avatar_url.replace("?size=1024", "")
        )
        await ctx.send(embed=em)

    @commands.command()
    async def marry(self, ctx, *, user: discord.Member):
        """Marry a user."""
        if len(ctx.message.mentions) == 0:
            await ctx.send(":x: Mention the user you want to marry, baka!")
            return
        if user.id == ctx.author.id:
            await ctx.send(":x: I-I'll marry you! I-I mean, y-you can't marry yourself... baka!")
            return
        if get_married(ctx.author.id) is not None:
            await ctx.send(":x: You are already married!")
            return
        if get_married(user.id) is not None:
            await ctx.send(":x: That user is already married!")
            return
        if user.bot:
            await ctx.send(":x: You can't marry a bot >~>")
            return
        await ctx.send(
            f"{user.display_name}, say `yes` or `no` to the marriage proposal from {ctx.author.display_name}")

        def check(m):
            return m.author.id == user.id and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for('message', check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await ctx.send("Proposal timed out :(")
        else:
            if msg.content.lower() == 'no':
                await ctx.send("Proposal denied. :(")
            elif msg.content.lower() == 'yes':
                db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'],
                                     config['db']['name'], charset='utf8mb4')
                cur = db.cursor()
                cur.execute(
                    f'INSERT INTO profiles (userid, description, bal, marryid, reps) VALUES ({ctx.author.id}, NULL, 0, {user.id}, 0) ON DUPLICATE KEY UPDATE marryid = {user.id}')
                cur.execute(
                    f'INSERT INTO profiles (userid, description, bal, marryid, reps) VALUES ({user.id}, NULL, 0, {ctx.author.id}, 0) ON DUPLICATE KEY UPDATE marryid = {ctx.author.id}')
                await ctx.send(f":tada: {ctx.author.display_name} and {user.display_name} are now married!")
                db.commit()
                db.close()
            else:
                await ctx.send("Improper response, cancelling proposal.")

    @commands.command()
    async def divorce(self, ctx):
        """Divorce yourself from the person you are married to."""
        if get_married(ctx.author.id):
            user = get_married(ctx.author.id)
            db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'],
                                 config['db']['name'], charset='utf8mb4')
            cur = db.cursor()
            cur.execute(
                f'INSERT INTO profiles (userid, description, bal, marryid, reps) VALUES ({ctx.author.id}, NULL, 0, NULL, 0) ON DUPLICATE KEY UPDATE marryid = NULL')
            cur.execute(
                f'INSERT INTO profiles (userid, description, bal, marryid, reps) VALUES ({user}, "{get_description(user)}", {get_balance(user)}, NULL, 0) ON DUPLICATE KEY UPDATE marryid = NULL')
            await ctx.send(":white_check_mark: You're single now I guess. That's nice.")
            db.commit()
            db.close()
        else:
            await ctx.send(":x: You can't get a divorce if you aren't married.")

    @commands.command(aliases=["desc"])
    async def description(self, ctx, *, description: str):
        """Set your description for your profile."""
        if len(description) >= 300:
            await ctx.send(":x: That description is too long! Max is 300 characters.")
            return
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        descri = description.replace('"', '\"')
        cur.execute(
            f'INSERT INTO profiles (userid, description, bal, marryid, reps) VALUES ({ctx.author.id}, "{descri}", 0, NULL, 0) ON DUPLICATE KEY UPDATE description = "{descri}"')
        db.commit()
        db.close()
        await ctx.send(":tada: Set your description. Check it out on `{}profile`!".format(ctx.prefix))

    @commands.group(aliases=['top', 'leaderboard'])
    async def richest(self, ctx):
        """Check the richest users.

        You can also check `richest rep`"""
        if ctx.invoked_subcommand is None:
            db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                                 charset='utf8mb4')
            cur = db.cursor()
            cur.execute(f'SELECT userid,bal FROM profiles ORDER BY bal DESC LIMIT 15')
            results = cur.fetchall()
            msg = ""
            for i in range(len(results)):
                row = results[i]
                user = self.bot.get_user(int(row[0]))
                if user is None:
                    user = row[0]
                n = i + 1
                if n < 10:
                    n = f"0{i+1}"
                msg += f":star: **{n} | {user}** - ${row[1]}\n"
            em = discord.Embed(
                title="Richest Users",
                description=msg,
                color=ctx.author.color
            )
            await ctx.send(embed=em)

    @richest.command(name="rep")
    async def _rep(self, ctx):
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        cur.execute(f'SELECT userid,reps FROM profiles ORDER BY reps DESC LIMIT 15')
        results = cur.fetchall()
        msg = ""
        for i in range(len(results)):
            row = results[i]
            user = self.bot.get_user(int(row[0]))
            if user is None:
                user = row[0]
            n = i + 1
            if n < 10:
                n = f"0{i+1}"
            msg += f":star: **{n} | {user}** - {row[1]} points\n"
        em = discord.Embed(
            title="Richest Users in Reputation",
            description=msg,
            color=ctx.author.color
        )
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(rate=1, per=43200, type=commands.BucketType.user)
    async def rep(self, ctx, *, user: discord.Member):
        """Rep a user."""
        if user.id == ctx.author.id:
            await ctx.send(":x: B-baka! You can't rep yourself.")
            ctx.command.reset_cooldown(ctx)
            return
        if user.bot:
            await ctx.send(":x: Bots can't be repped.")
            ctx.command.reset_cooldown(ctx)
            return
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        cur.execute(
            f'INSERT INTO profiles (userid, description, bal, marryid, reps) VALUES ({user.id}, NULL, 0, NULL, 1) ON DUPLICATE KEY UPDATE reps = reps + 1')
        db.commit()
        db.close()
        await ctx.send(f":ok_hand: Added one reputation point to **{user.display_name}**")

    @commands.command()
    @commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
    async def gamble(self, ctx, amount: int):
        """Gamble your money away."""
        if amount > get_balance(ctx.author.id):
            await ctx.send(":x: B-baka! You can't gamble more than what you have!")
            ctx.command.reset_cooldown(ctx)
            return
        if amount <= 0:
            await ctx.send(":x: Seriously...")
            ctx.command.reset_cooldown(ctx)
            return
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        var = random.randint(1, 3)
        if var == 2:
            cur.execute(f'UPDATE profiles SET bal = bal + {round(0.75 * amount)} WHERE userid = {ctx.author.id}')
            await ctx.send(f":tada: Congratulations, you won **${round(0.75 * amount)}** and got to keep what you had!")
        else:
            cur.execute(f'UPDATE profiles SET bal = bal - {amount} WHERE userid = {ctx.author.id}')
            await ctx.send(f":sob: You lost {amount} credits!")
        db.commit()
        db.close()

    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def transfer(self, ctx, user: discord.Member, amount: int):
        """Transfer money to another user."""
        if user.id == ctx.author.id:
            await ctx.send(":x: Baka! You can't transfer to yourself.")
            return
        if user.bot:
            await ctx.send(":x: You can't transfer to a bot.")
            return
        if amount > get_balance(ctx.author.id):
            await ctx.send(":x: You're broke.")
            return
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        cur.execute(
            f'INSERT INTO profiles (userid, description, bal, marryid, reps) VALUES ({user.id}, NULL, {amount}, NULL, 0) ON DUPLICATE KEY UPDATE bal = bal + {amount}')
        cur.execute(f'UPDATE profiles SET bal = bal - {amount} WHERE userid = {ctx.author.id}')
        db.commit()
        db.close()
        await ctx.send(f":ok_hand: Transfered **${amount}** to **{user.display_name}**")

    @commands.command()
    @commands.cooldown(rate=1, per=150, type=commands.BucketType.user)
    async def bet(self, ctx, colour: str, amount: int):
        """Bet on a horse race using the colour of the horse."""
        winmsgs = [
            "You bet ${0} on the {1} horse and won {2} credits!",  # .format(amount, colour, gains)
            "You bet ${0} on the {1} horse...\n\nIt was a close match, but the {1} horse won, making you win {2} credits!",
            "You wanted to bet ${0} on the horse your friend chose, but instead you bet on the {1} horse. You won {2} credits anyway!"
        ]
        losemsgs = [
            "You bet ${0} on the {1} horse, but the {2} horse won instead. You lost your bet.",
            "You went with your friend's vote of the {1} horse, betting ${0}, but you lost your bet when the {2} horse won.",
            "You bet ${0} on the {1} horse, but {2} won instead."
        ]
        colours = ["red", "green", "blue"]
        if amount > get_balance(ctx.author.id):
            await ctx.send(":x: B-baka! You can't gamble more than what you have!")
            ctx.command.reset_cooldown(ctx)
            return
        if not colour.lower() in colours:
            await ctx.send(
                ":x: I-I'm sorry, that is not a valid colour! The valid options are: `{}`".format("`, `".join(colours)))
            ctx.command.reset_cooldown(ctx)
            return
        if amount <= 0:
            await ctx.send(":x: Seriously...")
            ctx.command.reset_cooldown(ctx)
            return
        c = random.choice(colours)
        gains = (amount * 0.80)
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        if c == colour.lower():
            await ctx.send(f":tada: {random.choice(winmsgs).format(amount, colour, round(gains))}")
            cur.execute(f'UPDATE profiles SET bal = bal + {round(gains)} WHERE userid = {ctx.author.id}')
        else:
            await ctx.send(f":sob: {random.choice(losemsgs).format(amount, colour, c)}")
            cur.execute(f'UPDATE profiles SET bal = bal - {amount} WHERE userid = {ctx.author.id}')
        db.commit()
        db.close()

    @commands.command()
    @commands.cooldown(rate=1, per=43200, type=commands.BucketType.user)
    async def crime(self, ctx):
        """Commit a crime! This has a larger chance of failing but has a lower ratelimit than daily with a higher payout.
        Note: this command requires you to have a minimum balance of $300!"""
        losses = [
            "You took candy from a baby... and felt bad about it. You lost ${}.",
            "You got caught by the FBI. Pay ${} to get out of jail",
            "Your memes are terrible. You get ${} taken away because of it."
        ]
        wins = [
            "You successfully robbed a bank for ${}.",
            "You did the thing. Congratulations. You got ${}"
        ]
        n = random.randint(1, 5)
        if get_balance(ctx.author.id) < 300:
            await ctx.send(":x: You can't commit a crime without the $300 to fund it.")
            return
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        money = random.randint(150, 300)
        if n == 1:
            await ctx.send(f":tada: {random.choice(wins).format(money)}")
            cur.execute(f'UPDATE profiles SET bal = bal + {money} WHERE userid = {ctx.author.id}')
        else:
            cur.execute(f'UPDATE profiles SET bal = bal - {money} WHERE userid = {ctx.author.id}')
            await ctx.send(f":sob: {random.choice(losses).format(money)}")
        db.commit()
        db.close()


def setup(bot):
    bot.add_cog(Currency(bot))
