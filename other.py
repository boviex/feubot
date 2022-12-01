import discord
from discord.ext import commands
import os
from pickle import dump, load
import pickle
from functools import reduce
import cloudinary, cloudinary.uploader, cloudinary.api, urllib
import messageManager as msgManager

developerIDs = (91393737950777344, 171863408822452224, 146075481534365697)
developerCheck = commands.check(lambda x: x.message.author.id in developerIDs)

cl_name = os.environ.get('CLOUDNAME', default=None)
cl_key = os.environ.get('CLOUDKEY', default=None)
cl_secret = os.environ.get('CLOUDSECRET', default=None)

#assume if name is not set then none are set
if cl_name is None:
    cl_name, cl_key, cl_secret = open('./clcreds').read().replace('\n','').split(';')

cloudinary.config( 
  cloud_name = cl_name, 
  api_key = cl_key, 
  api_secret = cl_secret 
)

class Other(commands.Cog):
    """Commands added for convienience."""
    def __init__(self, bot):
        self.bot = bot
        try:
            #use cloud if available, fall back on local (i.e. what is in the repo)
            web_copy = cloudinary.api.resource("commands.pickle", resource_type='raw')['url']
            # try:
            response = urllib.request.urlopen(web_copy)
            print(response)
            self.dynamicCommands = load(response)
            if type(self.dynamicCommands) != dict:
                raise Exception
            print("Loaded pickle file from cloud")
            # except urllib.error.URLError as e:
            #     print(e)
            #     if os.path.exists("commands.pickle"):
            #         with open('commands.pickle', 'rb') as f:
            #             self.dynamicCommands = load(f)
            #             if type(self.dynamicCommands) != dict:
            #                 raise Exception
            #     else:
            #         self.dynamicCommands = dict()
        except Exception as e:
            print(e)
            print("Attempting to load local backup")
            try:
                if os.path.exists("commands_backup.pickle"):
                    with open('commands_backup.pickle', 'rb') as f:
                        self.dynamicCommands = load(f)
                        if type(self.dynamicCommands) != dict:
                            raise Exception
                        print("Backup loaded.")
                else:
                    print("Corrupted command pickle file! Loading nothing.\nException: %s" % e)
                    self.dynamicCommands = dict()
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
                f.close()
                result = cloudinary.uploader.upload('commands.pickle', resource_type='raw', public_id='commands.pickle', invalidate=True)

            with open('commands_backup.pickle', 'wb') as f:
                dump(self.dynamicCommands, f, pickle.HIGHEST_PROTOCOL)
                f.close()
                result = cloudinary.uploader.upload('commands_backup.pickle', resource_type='raw', public_id='commands_backup.pickle', invalidate=True)
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

    @commands.command()
    @developerCheck
    async def setReactionRole(self, ctx, messageID, role, reaction):
        """Admins only. Sets a reaction role on a specified message"""
        if messageID.isdigit():
            msgManager.add_role(str(messageID), reaction, role)
            await ctx.send(f"{role} for {reaction} reaction set")
        else:
            await ctx.send("Invalid messageID")

    @commands.command()
    @developerCheck
    async def unsetReactionRole(self, ctx, messageID, reaction):
        """
        Admins only. Removes a specified reaction role from a specified message.
        Using "ALL" as the role argument will remove all reaction roles
        """
        return_string = msgManager.delete_reaction_role(str(messageID), reaction)
        await ctx.send(return_string)

    @commands.command()
    async def listReactionRoles(self, ctx):
        """Lists messages with role reactions set along with what roles and reactions are usable"""
        return_string = ""

        reactRoles = msgManager.load_roles()

        if not reactRoles:
            await ctx.send("No reaction roles set")
            return

        #Loop through message dictionaries in reactRoles
        for a, b in reactRoles.items():
            messageID_link = None
            #loop through server channels to find matching message
            for guild in self.bot.guilds:
                for channel in guild.text_channels:
                    #Try to get message by ID
                    try:
                        messageID_link = await channel.fetch_message(a)
                        break
                    except (ValueError):
                        continue
                    except (discord.NotFound):
                        continue
                    except (discord.Forbidden):
                        continue

            #Display link to message if possible
            if messageID_link:
                return_string += f"<{messageID_link.jump_url}>:\n"
            else:
                return_string += f"{a}:\n"

            #Loop through reactions for the current message
            for x, y in b.items():
                if (discord.utils.get(ctx.guild.roles, name=y)):
                    return_string += f"        {x}: {y}\n"
                else:
                    return_string += f"        {x}: {y} | Does not exist\n"

        await ctx.send(return_string)

    @commands.command()
    @developerCheck
    async def setMessageProperty(self, ctx, messageID, newProperty):
        """Adnims only. Sets a property to a message"""
        if messageID.isdigit():
            msgManager.add_property(messageID, newProperty)
            await ctx.send(f"{newProperty} property set")
        else:
            await ctx.send("Invalid messageID")

    @commands.command()
    @developerCheck
    async def unsetMessageProperty(self, ctx, messageID, newProperty):
        """
        Adnins only. Removes a property from a message
        Using "ALL" as the property argument will remove all properties for the message
        """
        return_string = msgManager.delete_property(str(messageID), newProperty)
        await ctx.send(return_string)

    @commands.command()
    #@developerCheck
    async def listMessageProperties(self, ctx):
        return_string = ""

        properties = msgManager.load_properties()

        if not properties:
            await ctx.send("No properties set")
            return

        for a, b in properties.items():
             #loop through server channels to find matching message
            for guild in self.bot.guilds:
                for channel in guild.text_channels:
                    #Try to get message by ID
                    try:
                        messageID_link = await channel.fetch_message(a)
                        break
                    except (ValueError):
                        continue
                    except (discord.NotFound):
                        continue
                    except (discord.Forbidden):
                        continue

            #Display link to message if possible
            if messageID_link:
                return_string += f"<{messageID_link.jump_url}>:\n"
            else:
                return_string += f"{a}:\n"

            for x, y in b.items():
                return_string += f"        {x}\n"

        await ctx.send(return_string)


    # @commands.command()
    # async def cltest(self, ctx):
    #     filename = "test2.txt"
    #     with open(filename, 'w+') as save_to:
    #         save_to.write("testing")
    #         save_to.close()
    #         result = cloudinary.uploader.upload(filename, resource_type='raw', public_id=filename[2:], invalidate=True)
    #     print("saved!")

async def setup(bot):
    await bot.add_cog(Other(bot))
