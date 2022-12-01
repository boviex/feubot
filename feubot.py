import discord
from discord.ext import commands
import asyncio
import re
import random
import os
from sys import argv
# from feubotFormatter import FeubotFormatter
from discord.ext.commands import DefaultHelpCommand

import messageManager as msgManager

async def setupBot(bot):
    import helpful, memes, reactions, other#, undelete
    await reactions.setup(bot)
    await memes.setup(bot)
    await helpful.setup(bot)
    # undelete.setup(bot)
    await other.setup(bot)
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

    intents = discord.Intents.all()
    intents.members = True

    if "--debug" in argv:
        bot = commands.Bot(command_prefix=['##', 'feubeta '], description='this is feubot beta.', intents=intents, help_command = DefaultHelpCommand(dm_help=True))
    else:
        bot = commands.Bot(command_prefix=['!', '>>', 'feubot '], description='this is feubot.', intents=intents, help_command = DefaultHelpCommand(dm_help=True))

    @bot.event
    async def on_ready():
        await setupBot(bot)
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')
        await bot.change_presence(activity=discord.Game(name="Reading the doc!"))

    @bot.event
    async def on_raw_reaction_add(payload):
        messageID = payload.message_id
        reaction  = payload.emoji.name
        role_name = msgManager.find_role(str(messageID), reaction)
        msg_properties = msgManager.get_properties(str(messageID))

        guild  = bot.get_guild(payload.guild_id)
        member = payload.member
        role   = discord.utils.get(guild.roles, name=role_name)

        #Extra check for management uses
        if member == guild.owner and "ignoreOwner" in msg_properties:
            print("Ignoring owner")
            return

        if role:
            #If roles are exclusive, remove all other roles from the user
            if "exclusiveRoles" in msg_properties:
                reactRoles = msgManager.load_roles()[str(messageID)].values()
                for x in member.roles:
                    if x.name in reactRoles:
                        await member.remove_roles(x)

                #Remove other reactions on the message from this user
                message = await guild.get_channel(payload.channel_id).fetch_message(messageID)
                for x in message.reactions:
                    if x.emoji != reaction:
                        await x.remove(member)

            await member.add_roles(role)

    @bot.event
    async def on_raw_reaction_remove(payload):
        messageID = payload.message_id
        reaction  = payload.emoji.name
        role_name = msgManager.find_role(str(messageID), reaction)
        msg_properties = msgManager.get_properties(str(messageID))

        guild  = bot.get_guild(payload.guild_id)
        #Use guild.get_member since payload.member is None on ReactionRemove
        member = guild.get_member(payload.user_id)
        role   = discord.utils.get(guild.roles, name=role_name)

        #Extra check for management uses
        if member == guild.owner and "ignoreOwner" in msg_properties:
            print("Ignoring owner")
            return

        if role:
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

    bot.run(token)
