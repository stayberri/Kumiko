import discord
import requests
import datetime
import random
import asyncio
import json
from discord.ext import commands
from .utils.db import *
from .utils.tools import *
from .utils import weeb

with open('config.json', 'r') as f:
    config = json.load(f)


class Fun:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="8ball")
    async def _8ball(self, ctx, *, question):
        """Consult the magic 8ball with a question!"""
        url = 'https://8ball.delegator.com/magic/JSON/' + question
        r = requests.get(url)
        j = r.json()
        q = j['magic']['question']
        a = j['magic']['answer']
        t = j['magic']['type']
        em = discord.Embed(description=f"**Question:** {q}\n**Answer:** {a}\n**Response Type:** {t}", color=0x00ff00)
        em.set_thumbnail(url="https://8ball.delegator.com/images/8ball.png")
        em.set_author(name="You consult the magic 8 ball...", icon_url=ctx.author.avatar_url.replace("?size=1024", ""))
        em.set_footer(text="Powered by 8ball.delegator.com")
        em.timestamp = datetime.datetime.now()
        await ctx.send(embed=em)

    @commands.command()
    @commands.cooldown(rate=1, per=15, type=commands.BucketType.user)
    async def bowling(self, ctx):
        """Play a round of bowling!"""
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        init = random.choice(range(11))
        if init == 10:
            await ctx.send(":bowling: Strike! You got all of the pins! Added 30 credits to your account.")
            cur.execute(
                f'INSERT INTO profiles (userid, description, bal, marryid, reps) VALUES ({ctx.author.id}, NULL, 30, NULL, 0) ON DUPLICATE KEY UPDATE bal = bal + 30')
        else:
            await ctx.send(
                ":bowling: You tried to get a strike, but you ended up getting **{}** pins instead. Let's try again.".format(
                    init))
            second = random.choice(range(10 - init))
            if init + second == 10:
                await ctx.send(
                    ":bowling: You got a spare! ({} then {}) Added 10 credits to your account.".format(init, second))
                cur.execute(
                    f'INSERT INTO profiles (userid, description, bal, marryid, reps) VALUES ({ctx.author.id}, NULL, 10, NULL, 0) ON DUPLICATE KEY UPDATE bal = bal + 10')
            else:
                await ctx.send(
                    ":bowling: You didn't win, but you knocked down **{}** pins! ({} then {})".format(init + second,
                                                                                                      init, second))
        db.commit()
        db.close()

    @commands.command()
    async def choose(self, ctx, *choices):
        """Choose a random item from a list."""
        if len(choices) < 2:
            await ctx.send(":x: I-I need at least two things to choose!")
            return
        await ctx.send(f":thinking: O-oh, you want me to choose? I guess I choose `{random.choice(choices)}`")

    @commands.command(aliases=["len"])
    async def length(self, ctx, *, string: str):
        """Determine the length of a string.
        Note that this does have a joke if the word "dick" is included. To avoid this, end the string with '--bypass'"""
        if 'dick' in string.lower():
            if not string.lower().endswith('--bypass'):
                await ctx.send("\N{CROSS MARK} That is too " + ("small" if 'lars' not in string.lower() else 'long'))
            else:
                await ctx.send(
                    "\N{WHITE HEAVY CHECK MARK} That string is `{}` characters long (excluding the bypass)".format(
                        len(string) - 9))
        else:
            await ctx.send(f"\N{WHITE HEAVY CHECK MARK} The string you gave me is `{len(string)}` characters long.")

    @commands.command()
    async def trivia(self, ctx, *, difficulty: str = None):
        """Play a game of trivia. If you win, you will gain 45 credits."""
        db = pymysql.connect(config['db']['ip'], config['db']['user'], config['db']['password'], config['db']['name'],
                             charset='utf8mb4')
        cur = db.cursor()
        url = "https://opentdb.com/api.php?amount=1"
        if difficulty:
            url += "&difficulty=" + difficulty
        r = requests.get(url)
        j = r.json()
        correct = remove_html(j['results'][0]['correct_answer'])
        x = j['results'][0]['incorrect_answers']
        x.append(correct)
        y = []
        for val in x:
            val = remove_html(val)
            y.append(val)
        z = sorted(y, key=lambda l: l.lower())
        em = discord.Embed(description=remove_html(j['results'][0]['question']), color=ctx.author.color)
        em.add_field(name="Category", value=j['results'][0]['category'])
        em.add_field(name="Difficulty", value=j['results'][0]['difficulty'])
        em.add_field(name="Answers", value=("\n".join(z)), inline=False)
        await ctx.send(embed=em)
        dif = j['results'][0]['difficulty']
        if dif == "easy":
            money = 20
        elif dif == "medium":
            money = 40
        elif dif == "hard":
            money = 60

        def check1(m):
            return m.author.id == ctx.author.id and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for('message', check=check1, timeout=120.0)
        except asyncio.TimeoutError:
            await ctx.send("You didnt answer in time, the correct answer was `{}`".format(corect))
            return
        if msg.content.lower() == correct.lower():
            await ctx.send(":white_check_mark: **{}** got the correct answer and won **${}** credits!".format(
                ctx.author.display_name, money))
            cur.execute(
                f'INSERT INTO profiles (userid, description, bal, marryid, reps) VALUES ({ctx.author.id}, NULL, {money}, NULL, 0) ON DUPLICATE KEY UPDATE bal = bal + {money}')
            db.commit()
            db.close()
            return
        elif msg.content.lower() == "end":
            await ctx.send(f":ok_hand: Ended your game, the correct answer was `{correct}`")
            return
        else:
            if len(j['results'][0]['incorrect_answers']) > 2:
                await ctx.send(":x: That isn't right. You have one more try.")

                def check2(m):
                    return m.author.id == ctx.author.id and m.channel == ctx.channel

                try:
                    msg2 = await self.bot.wait_for('message', check=check2, timeout=120.0)
                except asyncio.TimeoutError:
                    await ctx.send("You didnt answer in time, the correct answer was `{}`".format(correct))
                    return
                if msg2.content.lower() == correct.lower():
                    await ctx.send(":white_check_mark: **{}** got the correct answer and won **${}** credits!".format(
                        ctx.author.display_name, money))
                    cur.execute(
                        f'INSERT INTO profiles (userid, description, bal, marryid, reps) VALUES ({ctx.author.id}, NULL, {money}, NULL, 0) ON DUPLICATE KEY UPDATE bal = bal + {money}')
                    db.commit()
                    db.close()
                    return
                elif msg2.content.lower() == "end":
                    await ctx.send(f":ok_hand: Ended your game, the correct answer was `{correct}`")
                    return
                else:
                    await ctx.send(":x: That's not right. The correct answer was `{}`".format(correct))
            else:
                await ctx.send(":x: That's not right. The correct answer was `{}`".format(correct))

    @commands.command()
    async def reverse(self, ctx, *, message):
        """Reverse a message that you give to me."""
        r = message[::-1]
        r = r.replace("@everyone", "no u").replace("@here", "no me")
        await ctx.send(r)

    @commands.command()
    async def achievement(self, ctx, *, text: str):
        """Generate a minecraft achievement."""
        num = random.randint(1, 26)
        weeb.save_to_image(url=f'https://www.minecraftskinstealer.com/achievement/a.php?i={num}&h=Achievement+Get%21&t={text.replace(" ", "+")}',
                           name='achievement.png')
        await ctx.send(file=discord.File('./images/achievement.png'))

    @commands.command()
    async def love(self, ctx, *members: discord.Member):
        """Use some magic numbers to calculate the compatibility between two users.
        If only one user is given, you will be used as the second."""
        l = members
        if len(members) > 2:
            l = [members[0], members[1]]
        if len(members) == 1:
            l = [ctx.author, members[0]]
        if len(members) == 0:
            return await ctx.send(":x: You need to specify the two users or one to compare with yourself.")
        if (l[0].id == l[1].id) and l[0].id != ctx.author.id:
            sum = 101
            msg = f"Be sure to tell {l[0].display_name} that they should love themself!"
        elif (l[0].id == l[1].id) and l[0].id == ctx.author.id:
            sum = 9001
            msg = "You are a special creature and should love yourself <3"
        else:
            sum = (l[0].id + l[1].id) % 101
            if sum == 0:
                msg = "Horrible match."
            elif 0 < sum < 21:
                msg = "Kinda bad."
            elif 20 < sum < 41:
                msg = "Could be much better."
            elif 40 < sum < 61:
                msg = "Not bad, not bad at all."
            elif 60 < sum < 81:
                msg = "Pretty good if you ask me."
            elif 80 < sum < 91:
                msg = "Really, really good."
            elif 90 < sum < 100:
                msg = "As close to perfect as you can get!"
            else:
                msg = "Absolutely ideal and perfect!"
            names = [l[0].display_name, l[1].display_name]
            shipname = names[0][:int(len(names[0])/2)] + names[1][int(len(names[1])/2):]
        em = discord.Embed(
            title="Love Meter",
            description=f"\N{TWO HEARTS} **{l[0].display_name}**\n\N{TWO HEARTS} **{l[1].display_name}**",
            color=ctx.author.color)
        em.add_field(name="Result", value=f"**{sum}%**\n`{msg}`", inline=False)
        em.add_field(name="Shipname", value=shipname)
        em.set_thumbnail(url="https://www.emojibase.com/resources/img/emojis/hangouts/1f49c.png")
        await ctx.send(embed=em)



def setup(bot):
    bot.add_cog(Fun(bot))
