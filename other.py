import discord
from discord.ext import commands
import os
from pickle import dump, load
import pickle
from functools import reduce

developerIDs = (91393737950777344, 171863408822452224, 146075481534365697)

developerCheck = commands.check(lambda x: x.message.author.id in developerIDs)

class Other(commands.Cog):
    """Commands added for convienience."""
    def __init__(self, bot):
        self.bot = bot
        try:
            if os.path.exists("commands.pickle"):
                with open('commands.pickle', 'rb') as f:
                    self.dynamicCommands = load(f)
                    if type(self.dynamicCommands) != dict:
                        raise Exception
            else:
                self.dynamicCommands = dict()
        except Exception as e:
            try:
                if os.path.exists("commands_backup.pickle"):
                    with open('commands_backup.pickle', 'rb') as f:
                        self.dynamicCommands = load(f)
                        if type(self.dynamicCommands) != dict:
                            raise Exception
                else:
                    print("Corrupted command pickle file! Loading nothing.\nException: %s" % e)
            except Exception as e2:
                print("Corrupted command pickle file and backup! Loading nothing.\nException: %s\n%s" % (e, e2))
            self.dynamicCommands = dict()

        for command in self.dynamicCommands:
            # Add a layer of function abstraction to store a context-local variable
            def makeCommand():
                localCommand = command # Store for when command changes.
                @self.bot.command(name = localCommand, cog_name = "Other")
                async def local(ctx):
                    await ctx.send(self.dynamicCommands[localCommand])
            # And call it.
            try:
                makeCommand()
            except:
                pass

        async def developerError(self, error, ctx):
            if type(error) == commands.CheckFailure:
                await ctx.send('You are not authorized to use that command.')
        self.addCommand.error(developerError)
        self.removeCommand.error(developerError)
        self.save.error(developerError)
        self.botEval.error(developerError)

    @commands.command(ignore_extra = False)
    @developerCheck
    async def addCommand(self, ctx, command_name, command_content):
        """Admins only. Adds a new simple response command."""
        if str(command_name).casefold() in map(lambda x: str(x).casefold(), self.bot.commands):
            await ctx.send("Command name conflicts with existing command.")
            return

        self.dynamicCommands[command_name] = command_content
        @self.bot.command(name = command_name, cog_name = "Other")
        async def local(ctx):
            await ctx.send(command_content)
        await ctx.send("Added command \"%s\"." % command_name)

    @commands.command(ignore_extra = False)
    @developerCheck
    async def removeCommand(self, ctx, command_name):
        """Admins only. Removes a previously defined simple response command."""
        if command_name not in self.dynamicCommands:
            await ctx.send("Custom command does not exist.")
            return
        del self.dynamicCommands[command_name]
        self.bot.remove_command(command_name)
        await ctx.send("Command \"%s\" successfully deleted." % command_name)

    @commands.command()
    @developerCheck
    async def save(self, ctx):
        """Admins only. Saves all of the current custom commands to be loaded when FEUbot is booted."""
        try:
            with open('commands.pickle', 'wb') as f:
                # Pickle the 'data' dictionary using the highest protocol available.
                dump(self.dynamicCommands, f, pickle.HIGHEST_PROTOCOL)

            with open('commands_backup.pickle', 'wb') as f:
                dump(self.dynamicCommands, f, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            await ctx.send("Error saving commands.\nException: %s" % e)
            return
        await ctx.send("Commands successfully saved.")

    @commands.command(name = 'eval')
    @developerCheck
    async def botEval(self, ctx, *, arg):
        """Admins only. Evaluate a Python code segment. UNSAFE!!!"""
        fix = lambda f: (lambda x: x(x))(lambda y: f(lambda args: y(y)(args)))
        try:
            res = eval(arg, __builtins__, { "fix" : fix , "reduce" : reduce })
            await ctx.send(str(res))
        except SystemExit:
            await ctx.send("I tried to quit().")

def setup(bot):
    bot.add_cog(Other(bot))
