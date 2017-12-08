import discord
import hastebin
import io
import textwrap
from contextlib import redirect_stdout
from discord.ext import commands

ownerids = [267207628965281792]


class Owner():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="eval", hidden=True)
    async def _eval(self, ctx):
        args = ctx.message.content
        args = args.split(' ')
        if ctx.message.author.id not in ownerids:
            await ctx.send(":x: You do not have permission to evaluate code.")
            return
        try:
            if args[1] != "":
                if args[1] == "py":
                    code = ctx.message.content.replace(args[0] + " " + args[1] + " ", "")
                    code = code.strip('` ')
                elif args[1] == "js":
                    code = ctx.message.content.replace(args[0] + " " + args[1] + " ", "")
                    javascript = 'Excecuted successfully and returned: {}'
                    try:
                        result = js2py.eval_js(str(code))
                        if result is None:
                            a = "Executed successfully with no objects returned."
                        else:
                            a = javascript.format(result)
                        await ctx.send(
                            embed=discord.Embed(description=a, color=0x00ff00).set_author(name="Evaluated with success",
                                                                                          icon_url=ctx.message.author.avatar_url.replace(
                                                                                              "?size=1024",
                                                                                              "")).set_footer(
                                text="Executed by: " + str(ctx.message.author)).set_thumbnail(
                                url='http://www.iconsdb.com/icons/preview/green/checked-checkbox-xxl.png').add_field(
                                name="Code", value="[See here.]({})".format(hastebin.post(code))))
                        return
                    except Exception as e:
                        await ctx.send(embed=discord.Embed(
                            description="Excecuted and errored: {}".format(type(e).__name__ + ': ' + str(e)),
                            color=0xff0000).set_author(name="Evaluated and errored",
                                                       icon_url=ctx.message.author.avatar_url.replace("?size=1024",
                                                                                                      "")).set_footer(
                            text="Executed by: " + str(ctx.message.author)).set_thumbnail(
                            url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Red_x.svg/480px-Red_x.svg.png').add_field(
                            name="Code", value="[See here.]({}.js)".format(hastebin.post(code))))
                        return
                else:
                    code = ctx.message.content.replace(args[0] + " ", "")
                    code = code.strip('` ')
                env = {
                    'self': self,
                    'bot': self.bot,
                    'ctx': ctx,
                    'message': ctx.message,
                    'guild': ctx.guild,
                    'channel': ctx.channel,
                    'author': ctx.author,
                    'me': ctx.me
                }
                env.update(globals())

                stdout = io.StringIO()

                toCompile = f'async def func():\n{textwrap.indent(code, "  ")}'

                try:
                    exec(toCompile, env)
                except Exception as e:
                    em = discord.Embed(description=f"Excecuted and errored: {e.__class__.__name__}: {e}",
                                       color=0xff0000)
                    em.set_author(name="Evaluated and errored",
                                  icon_url=ctx.message.author.avatar_url.replace("?size=1024", ""))
                    em.set_footer(text="Executed by: " + str(ctx.message.author))
                    em.set_thumbnail(
                        url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Red_x.svg/480px-Red_x.svg.png')
                    em.add_field(name="Code", value=f"[See here.]({hastebin.post(code)}.py)")
                    return await ctx.send(embed=em)

                func = env['func']
                try:
                    with redirect_stdout(stdout):
                        ret = await func()
                except Exception as e:
                    value = stdout.getvalue()
                    em = discord.Embed(description=f"Excecuted and errored: ```py\n{value}{traceback.format_exc()}```",
                                       color=0xff0000)
                    em.set_author(name="Evaluated and errored",
                                  icon_url=ctx.message.author.avatar_url.replace("?size=1024", ""))
                    em.set_footer(text="Executed by: " + str(ctx.message.author))
                    em.set_thumbnail(
                        url='https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Red_x.svg/480px-Red_x.svg.png')
                    em.add_field(name="Code", value=f"[See here.]({hastebin.post(code)}.py)")
                    await ctx.send(embed=em)
                else:
                    value = stdout.getvalue()
                    if ret is None or type(ret) is discord.Message:
                        if value:
                            x = f"{value}"
                        else:
                            x = "Executed successfully with no objects returned."
                    else:
                        x = f"Executed successfully and returned: {value}{ret}"
                    em = discord.Embed(description=x, color=0x00ff00)
                    em.set_author(name="Evaluated with success",
                                  icon_url=ctx.message.author.avatar_url.replace("?size=1024", ""))
                    em.set_footer(text="Executed by: " + str(ctx.message.author))
                    em.set_thumbnail(url='http://www.iconsdb.com/icons/preview/green/checked-checkbox-xxl.png')
                    em.add_field(name="Code", value=f"[See here.]({hastebin.post(code)}.py)")
                    await ctx.send(embed=em)
        except IndexError:
            await ctx.send(":x: Specify code to evaluate")

def setup(bot):
    bot.add_cog(Owner(bot))