import discord
from discord.ext import commands
import asyncio
import re
import random
import urllib
import urllib.request
import urllib.error
import os
import json

#bot = commands.Bot(command_prefix=['!', '>>', 'feubot '], description='this is feubot.')

bot = commands.Bot(command_prefix=['##', 'feubeta '], description='this is feubot beta.')

def trunc_to(ln, s):
    if len(s) <= ln: return s
    else: return s[:ln-3] + "..."

def highlight(s, term):
    to_bold = term.split(' ')
    output = re.sub(r'(%s)' % '|'.join(to_bold), r'**\1**', s, flags=re.IGNORECASE)
    return output

def capitalise(s, term):
    to_bold = term.split(' ')
    output = re.sub(r'(%s)' % '|'.join(to_bold), lambda match: r'{}'.format(match.group(1).upper()), s, flags=re.IGNORECASE)
    return output

def linkify(searchtext):
    feu_post_base = "http://feuniverse.us/t/{}/{}"
    def result(data):
        post, thread = data
        title = capitalise(thread['title'], searchtext)
        blurb = highlight(trunc_to(50,post['blurb']), searchtext)
        link = '[Post in %s](%s)' % (
                title,
                feu_post_base.format(post['topic_id'], post['post_number']))
        threadline = '**%s by %s**' % (link, post['username'])
        return threadline + '\n' + blurb
    return result

def create_embed(posts, threads, term):
    feu_search_base = "http://feuniverse.us/search?q=%s"
    searchtext = urllib.parse.unquote(term)

    numresults = 5

    result = discord.Embed(
            title='Search results for "%s"' % urllib.parse.unquote(term),
            url=feu_search_base % term,
            color=0xde272c)
    innerEmbed = '\n\n'.join(
            map(linkify(searchtext),zip(posts[:numresults],threads)))
    result.add_field(
            name='Found %d result(s)' % len(posts),
            value=innerEmbed,
            inline=False)
    if len(posts) > numresults:
        result.set_footer(
                text="Truncated %d result(s)." % (len(posts)-numresults))
    return result

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name="Reading the doc!"))

@bot.command()
async def search(*, term):
    """search feu"""
    root = "http://feuniverse.us/search.json?q=%s"
    payload = urllib.parse.quote(term)
    with urllib.request.urlopen(root % payload) as query:
        try:
            data = json.loads(query.read().decode())
            posts = data["posts"]
            threads = data["topics"]
            await bot.say(embed=create_embed(posts, threads, payload))
        except urllib.error.URLError:
            await bot.say("Error accessing FEU server, please try again later.")
        except KeyError:
            await bot.say(embed=create_embed(posts, [], payload))

@bot.command()
async def donate():
    """you know it"""
    await bot.say("https://donorbox.org/donate-to-circles")

@bot.command()
async def UT2():
    """links ultimate tutorial v2"""
    embed=discord.Embed(title="Fire Emblem Hacking Ultimate Tutorial v2", url='https://stackedit.io/viewer#!provider=gist&gistId=084645b0690253600f4aa2a57b76a105&filename=feutv2', description="How to do everything with Event Assembler buildfiles", color=0x40caf2)
    await bot.say(embed=embed)
@bot.command()
async def reply():
    """r e p l y s o o n"""
    await bot.say("reply :soon: :smile:")

@bot.command()
async def fuckingincredible():
    """fuckingincredible.png"""
    await bot.say("http://i.imgur.com/yt4hXhJ.png")

@bot.command()
async def arch():
    """do something with arch"""
    direction = random.choice([":arrow_down:", ":arrow_up:"])
    await bot.say(direction+" with <:arch_mini:230160993299202068>")

@bot.command()
async def goofs():
    """list goofs"""
    filenameslist = [os.path.splitext(f)[0] for f in os.listdir("./goofs")]
    await bot.say("```"+"\n".join(map(str, filenameslist))+"```")

# @bot.command()
# async def goof(*args):
#     """show goof"""
#     requested = args
#     gooflist = os.listdir("./goofs")
#     if len(requested) != 0:
#         for request in requested:
#             if request in gooflist:
#                 await bot.upload("./goofs/"+request)
#             else:
#                 await bot.say("Use >>goofs to see a list of accepted goofs.")
#     else:
#         await bot.upload("./goofs/"+random.choice(gooflist))

@bot.command()
async def goof(*args):
    """show goof"""
    requested = args
    gooflist = {a.lower(): a for a in os.listdir("./goofs")}
    if len(requested) != 0:
        maxgoofs = 5
        for request in requested:
            if maxgoofs == 0: return
            else: maxgoofs -= 1
            file_extension_or_not_pattern = re.compile('(\.[a-z]+)?$', re.I | re.M)
            found = False
            for extension in ['.png', '.jpg', '.gif', '.jpeg']:
                request_file = file_extension_or_not_pattern.sub(extension, request).lower()
                if request_file in gooflist:
                    found = True
                    await bot.upload("./goofs/"+gooflist[request_file])
            if not found:
                await bot.say("Use >>goofs to see a list of accepted goofs.")
    else:
        await bot.upload("./goofs/"+random.choice([a for a in gooflist.values()]))

@bot.command()
async def ews():
    """disgusting list"""
    filenameslist = [os.path.splitext(f)[0] for f in os.listdir("./disgusting")]
    await bot.say("```"+"\n".join(map(str, filenameslist))+"```")

@bot.command()
async def ew(*args):
    """disgusting"""
    requested = args
    ewlist = {a.lower(): a for a in os.listdir("./disgusting")}
    if len(requested) != 0:
        maxews = 5
        for request in requested:
            if maxews == 0: return
            else: maxews -= 1
            file_extension_or_not_pattern = re.compile('(\.[a-z]+)?$', re.I | re.M)
            found = False
            for extension in ['.png', '.jpg', '.gif', '.jpeg']:
                request_file = file_extension_or_not_pattern.sub(extension, request).lower()
                if request_file in ewlist:
                    found = True
                    await bot.upload("./disgusting/"+ewlist[request_file])
            if not found:
                await bot.say("Use >>ews to see a list of accepted names.")
    else:
        await bot.upload("./disgusting/"+random.choice([a for a in ewlist.values()]))

@bot.command()
async def casual():
    """just play phoenix"""
    barflist = os.listdir("./casual")
    await bot.upload("./casual/"+random.choice(barflist))

@bot.command()
async def crackers():
    """jumping boat monkeys!"""
    await bot.upload("./Holy_crackers.png")

@bot.command()
async def hector():
    """judges you"""
    await bot.upload("./hectorpc.png")

@bot.command()
async def erin():
    """ERIN INTENSIFIES"""
    await bot.upload("./erinyous.gif")

@bot.command()
async def fury():
    """2 FAST 2 FURYOUS"""
    await bot.say("Don't you mean `>>erin`?")

@bot.command()
async def goldmine():
    """everything you ever wanted"""
    await bot.say("https://www.dropbox.com/sh/xl73trcck2la799/AAAMdpNSGQWEzYkLEQEiEhGFa?dl=0")

@bot.command()
async def hit(number, type="1RN"):
    """rolls hit or miss (e.g. >>hit 50 1rn[default]/2rn/fates)"""
    try:
        num = int(number)
    except ValueError:
        await bot.say("Specify an integer 0-100")
        return
    if (num < 0) or (num > 100):
        await bot.say("Specify an integer 0-100")
        return
    if type.upper()=="1RN":
        rolled = random.randint(1,100)
    elif type.upper()=="2RN":
        rolled = (random.randint(1,100) + random.randint(1,100))>>1
    elif type.upper()=="FATES":
        rolled = random.randint(1,100)
        if rolled > 50:
            rolled = ((rolled*3) + random.randint(1,100))>>2
    else:
        await bot.say("Valid types are 1RN, 2RN, Fates")
        return
    if rolled <= num: await bot.say("HIT (%d)" % rolled)
    else: await bot.say("MISS (%d)" % rolled)

@bot.command()
async def whois(*args):
    """roy is our boy"""
    if len(args) > 0:
        lord = ' '.join(args)
        if (lord.lower() in ['circles','circleseverywhere']):
            await bot.say(lord + " is my dad")
            return
        elif (lord.lower() == 'feditor'):
            await bot.say("`" + lord + " a shit`")
            return
        elif lord[0].lower() in 'bcdfghjklmnpqrstvwxz':
            blord = 'b'+lord[1:]
        else:
            blord = 'b'+lord
        await bot.say(lord + " is our " + blord)

@bot.command()
async def spritans():
    """REEE"""
    await bot.say("muh")
    await asyncio.sleep(1)
    await bot.say("SPRITANS")
    await asyncio.sleep(2)
    await bot.say("***REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE***")

@bot.command()
async def createwaifu(*args):
    """:wink:"""
    heads = [
        "<:zigludo:252132877678936064>", 
        "<:zahlman:230166256412655616>", 
        "<:narcian:271805925017387008>", 
        "<:marf:230171669635923968>", 
        "<:lloydwut:313590046978605059>", 
        "<:linde:325036388833558539>", 
        "<:lilina:230156179916062720>", 
        "<:kent:232283653642780672>", 
        "<:kaga:293121861905022976>", 
        "<:ick:280744571640610816>", 
        "<:florina:230904896067469312>", 
        "<:FEU:230151584846184448>", 
        "<:fa:303774076252454912>", 
        "<:elise:235616193065517066>", 
        "<:eliwood:232283812938121217>", 
        "<:elbert:232283825974149120>", 
        "<:EAmoe:317182514559188994>", 
        "<:doot:324593825815461889>", 
        "<:donate:230166446146191362>", 
        "<:doc:280527122802540544>", 
        "<:colorz:230159530158194688>", 
        "<:circles:238177111418863617>", 
        "<:celica:272027128231362571>", 
        "<:BBQ:230169373694885888>", 
        "<:arch_mini:230160993299202068>", 
        "<:cam_thumb:307559627573428224>", 
        "<:dat:292422389197701121>", 
        "<:thighs:294965155819683840>"]
    if len(args) > 0: head = ' '.join(args)
    else: head = random.choice(heads)
    await bot.say(head + """
<:personality:274564774979960832>
<:thighs:294965155819683840>""")

@bot.command()
async def doot():
    """doot doot"""
    flip = random.choice([0,1])
    if flip ==1:
        await bot.say("""<:doot:324593825815461889> <:doot:324593825815461889> :trumpet: :trumpet: :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: <:doot:324593825815461889> <:doot:324593825815461889> <:doot:324593825815461889>
<:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: <:doot:324593825815461889> :trumpet:
<:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: <:doot:324593825815461889> :trumpet:
<:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: <:doot:324593825815461889> :trumpet:
<:doot:324593825815461889> <:doot:324593825815461889> :trumpet: :trumpet: :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: :trumpet: <:doot:324593825815461889> :trumpet:""")
    else:
        await bot.upload("./DOOT.png")

@bot.command()
async def ea():
    """EVERYTHING ASSEMBLER"""
    everythingassemblerstring = """``` _____                 _   _   _         
|   __|_ _ ___ ___ _ _| |_| |_|_|___ ___ 
|   __| | | -_|  _| | |  _|   | |   | . |
|_____|\_/|___|_| |_  |_| |_|_|_|_|_|_  |
                  |___|             |___|
 _____                   _   _
|  _  |___ ___ ___ _____| |_| |___ ___
|     |_ -|_ -| -_|     | . | | -_|  _|
|__|__|___|___|___|_|_|_|___|_|___|_|```"""
    await bot.say(everythingassemblerstring)

token = os.environ.get('TOKEN', default=None)
if token is None:
    token = open('./token').read().replace('\n','')
bot.run(token)
