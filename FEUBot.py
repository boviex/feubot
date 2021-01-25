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


def create_embed(posts, threads, term):
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
            await ctx.send(embed=create_embed(posts, threads, payload))
        except urllib.error.URLError:
            await ctx.send("Error accessing FEU server, please try again later.")


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="Eating some beans."))

    

bot.run("NzgxNjA3NjcwNDc3ODgxMzQ0.X8AG3g.kXaBbw0y4Vidgp6u2Sjo7IKsFIg")
