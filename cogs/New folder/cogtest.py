import discord
from discord.ext import commands

class cogtestCog(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Test Cog is online')

    @commands.command()
    async def testing(self, ctx):
        await ctx.send("Testing 123")
        
def setup(bot):
    bot.add_cog(cogtestCog(bot))
