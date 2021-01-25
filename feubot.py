import discord
import os
from discord.ext import commands
import sys, traceback
from sys import argv
from dotenv import load_dotenv
import re
import random
import urllib
import urllib.request
import urllib.error
import json
from feubotFormatter import FeubotFormatter

bot = commands.Bot(command_prefix =  "!")

def trunc_to(ln, s):
    if len(s) >= ln: return s
    else: return s[:ln-3] + "..."


def feu_search_embed(posts, threads, term):
        feu_search_base = "http://feuniverse.us/search?q=%s"
        feu_post_base = "http://feuniverse.us/t/{}/{}"

        result = discord.Embed(
                title="Search results",
                url=feu_search_base % term,
                description="Found %d results" % len(posts),
                color=0xde272c)
        for i,post in enumerate(posts[:5]):
            result.add_field(
                    name='Post in "%s" by %s' % (threads[i]["title"], post["name"]),
                    value="[%s](%s)" %
                        (trunc_to(50, post["blurb"]),
                          feu_post_base.format(post["topic_id"], post["post_number"])),
                    inline=False)
        if len(posts) > 5:
            result.set_footer(text="Truncated %d result(s)." % (len(posts)-5))
        return result

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cogs.{extension}")

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cogs.{extension}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        
@bot.command()
async def search(ctx, *, term):
    """search feu"""
    root = "http://feuniverse.us/search.json?q=%s"
    payload = urllib.parse.quote(term)
    with urllib.request.urlopen(root % payload) as query:
        try:
            data = json.loads(query.read().decode())
            posts = data["posts"]
            threads = data["topics"]
            await ctx.send(embed=feu_search_embed(posts, threads, payload))
        except urllib.error.URLError:
            await ctx.send("Error accessing FEU server, please try again later.")


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="Eating some beans."))

    

bot.run("discordbotkey")
=======
import discord
from discord.ext import commands
import asyncio
import re
import random
import os
from sys import argv

from feubotFormatter import FeubotFormatter

def setupBot(bot):
    import helpful, memes, reactions, undelete, other
    bot.remove_cog("Reactions")
    bot.remove_cog("Memes")
    bot.remove_cog("Helpful")
    bot.remove_cog("UndeleteCog")
    bot.remove_cog("Other")
    reactions.setup(bot)
    memes.setup(bot)
    helpful.setup(bot)
    undelete.setup(bot)
    other.setup(bot)
    #TODO: Stuff like bot.other = bot.get_cog("Other") and such. Then initialize debug's "self" to be bot.

    bot.remove_command('debug')
    #Reload this as part of reload due to use of other.developerCheck
    @bot.command(pass_context=True, hidden = True, aliases = ['exec'])
    @other.developerCheck
    async def debug(ctx, *, arg):
        # https://stackoverflow.com/questions/3906232/python-get-the-print-output-in-an-exec-statement
        from io import StringIO
        import sys
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        bot = ctx.bot
        try:
            exec(arg)
        except SystemExit:
            await bot.say("I tried to quit().")
        finally:
            sys.stdout = old_stdout
        output = redirected_output.getvalue()
        output = "No output." if not output else output
        await bot.say(output)


if __name__ == "__main__":
    if "--debug" in argv:
        bot = commands.Bot(command_prefix=['##', 'feubeta '], description='this is feubot beta.', formatter = FeubotFormatter())
    else:
        bot = commands.Bot(command_prefix=['!', '>>', 'feubot '], description='this is feubot.', formatter = FeubotFormatter())

    @bot.event
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')
        await bot.change_presence(game=discord.Game(name="Reading the doc!"))

    @bot.add_listener
    async def on_command_error(error, ctx):
        if type(error) == commands.CheckFailure:
            pass
        elif type(error) == commands.CommandNotFound:
            pass
        else:
            await bot.send_message(ctx.message.channel, error)

    @bot.command()
    async def donate():
        """you know it"""
        await bot.say("https://www.patreon.com/theFEUfund")
        await bot.say("https://donorbox.org/donate-to-circles")

    token = os.environ.get('TOKEN', default=None)
    if token is None:
        token = open('./token').read().replace('\n','')

    bot.reload = lambda: setupBot(bot)
    setupBot(bot)
    bot.run(token)
