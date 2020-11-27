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
