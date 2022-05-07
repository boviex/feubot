import discord
from discord.ext import commands
import asyncio
import re
import random
import os
from sys import argv
# from feubotFormatter import FeubotFormatter
from discord.ext.commands import DefaultHelpCommand


def setupBot(bot):
    import helpful, memes, reactions, other#, undelete
    reactions.setup(bot)
    memes.setup(bot)
    helpful.setup(bot)
    # undelete.setup(bot)
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
            await bot.send("I tried to quit().")
        finally:
            sys.stdout = old_stdout
        output = redirected_output.getvalue()
        output = "No output." if not output else output
        await bot.send(output)


if __name__ == "__main__":

    intents = discord.Intents.default()
    intents.members = True

    if "--debug" in argv:
        bot = commands.Bot(command_prefix=['##', 'feubeta '], description='this is feubot beta.', intents=intents, help_command = DefaultHelpCommand(dm_help=True))
    else:
        bot = commands.Bot(command_prefix=['!', '>>', 'feubot '], description='this is feubot.', intents=intents, help_command = DefaultHelpCommand(dm_help=True))

    @bot.event
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')
        await bot.change_presence(activity=discord.Game(name="Reading the doc!"))

    @bot.event
    async def on_raw_reaction_add(payload):
        messageID = payload.message_id
        try:
            with open("BCRoleReaction.txt", "r") as file:
                reactMessage = int(file.read())

        except (FileNotFoundError, IOError):
            return

        if messageID == reactMessage:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

            if payload.emoji.name == "🐱":
                role = discord.utils.get(guild.roles, name="Catposting")
            elif payload.emoji.name == "🦎":
                role = discord.utils.get(guild.roles, name="Lizardposting")
            elif payload.emoji.name == "🐶":
                role = discord.utils.get(guild.roles, name="Dogposting")

            if role:
                member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                if member:
                    await member.add_roles(role)

    @bot.event
    async def on_raw_reaction_remove(payload):
        messageID = payload.message_id
        try:
            with open("BCRoleReaction.txt", "r") as file:
                reactMessage = int(file.read())

        except (FileNotFoundError, IOError):
            return

        if messageID == reactMessage:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

            if payload.emoji.name == "🐱":
                role = discord.utils.get(guild.roles, name="Catposting")
            elif payload.emoji.name == "🦎":
                role = discord.utils.get(guild.roles, name="Lizardposting")
            elif payload.emoji.name == "🐶":
                role = discord.utils.get(guild.roles, name="Dogposting")

            if role:
                member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
                if member:
                    await member.remove_roles(role)

    @bot.add_listener
    async def on_command_error(ctx, error):
        if type(error) == commands.CheckFailure:
            pass
        elif type(error) == commands.CommandNotFound:
            pass
        else:
            await ctx.message.channel.send(error)

    @bot.add_listener
    async def on_message(message):
        if message.channel.id == 746515160377851997: #prep_screen id
            bot_member = message.guild.get_member(bot.user.id)
            bot_role = discord.utils.get(message.guild.roles, name="Conscripter")
            if bot_role in bot_member.roles:
                if "soldier" in message.content.lower():
                    role = discord.utils.get(message.guild.roles, name="Soldier")
                    await message.author.add_roles(role)

    @bot.command()
    async def donate(ctx):
        """you know it"""
        await ctx.send("https://donate.tiltify.com/+fire-emblem-universe/fire-emblem-e3-2021")
        await ctx.send("https://www.patreon.com/theFEUfund")
        # await ctx.send("https://donorbox.org/donate-to-circles")

    token = os.environ.get('TOKEN', default=None)
    if token is None:
        token = open('./token').read().replace('\n','')

    bot.reload = lambda: setupBot(bot)
    setupBot(bot)
    bot.run(token)
