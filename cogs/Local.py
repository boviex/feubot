import discord
import random
import os
from sys import argv
from dotenv import load_dotenv
import asyncio
import urllib
import urllib.request
import urllib.error
import sys, traceback
import re
import json
from discord.ext import commands

class Local(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot    

    @commands.Cog.listener()
    async def on_ready(self):
        print('Local Cog is online')

    @commands.command()
    async def goof(self, ctx, *args):
         """show goof"""
         requested = args
         gooflist = os.listdir("./goofs")
         if len(requested) != 0:
             for request in requested:
                if request in gooflist:
                    await ctx.send(file=discord.File("./goofs/"+request))
                else:
                    await ctx.send("Use >>goofs to see a list of accepted goofs.")
         else:
             await ctx.send(file=discord.File("./goofs/"+random.choice(gooflist)))

        

    @commands.command()
    async def donate(self, ctx):
        """you know it"""
        await ctx.send("https://www.patreon.com/theFEUfund")
        await ctx.send("https://donorbox.org/donate-to-circles")


    @commands.command()
    async def UT2(self, ctx):
        """links ultimate tutorial v2"""
        await ctx.send("https://stackedit.io/viewer#!provider=gist&gistId=084645b0690253600f4aa2a57b76a105&filename=feutv2")

    @commands.command()
    async def reply(self, ctx):
        """r e p l y s o o n"""
        await ctx.send("reply :soon: :smile:")

    @commands.command()
    async def arch(self, ctx):
        """do something with arch"""
        direction = random.choice([":arrow_down:", ":arrow_up:", ":arrow_up_down:", ":question:", ":heart:"])
        await ctx.send(direction+" with <:arch_mini:230160993299202068>")

    @commands.command()
    async def goofs(self, ctx):
        """list goofs"""
        await ctx.send("```"+"\n".join(map(str, os.listdir("./goofs")))+"```")
    
    @commands.command()
    async def erin(self, ctx):
        """ERIN INTENSIFIES"""
        await ctx.send(file=discord.File("./erinyous.gif"))

    @commands.command()
    async def fury(self, ctx):
        """2 FAST 2 FURYOUS"""
        await ctx.send("Don't you mean `>>erin`?")

    @commands.command()
    async def doot(self, ctx):
        """doot doot"""
        await ctx.send("""<:doot:324593825815461889> <:doot:324593825815461889> :trumpet: :trumpet: :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: <:doot:324593825815461889> <:doot:324593825815461889> <:doot:324593825815461889>
    <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: <:doot:324593825815461889> :trumpet:
    <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: <:doot:324593825815461889> :trumpet:
    <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: <:doot:324593825815461889> :trumpet:
    <:doot:324593825815461889> <:doot:324593825815461889> :trumpet: :trumpet: :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: :trumpet: <:doot:324593825815461889> :trumpet:""")

            
def setup(bot):
    bot.add_cog(Local(bot))
