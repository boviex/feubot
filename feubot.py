import discord
from discord.ext import commands
import asyncio
import re
import random
import os
import urllib
import urllib.request
import urllib.error
from sys import argv
from discord.ext.commands import Bot
from dotenv import load_dotenv
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")

bot = Bot("!")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


from feubotFormatter import FeubotFormatter

def setupBot(bot):

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
        bot = commands.Bot(command_prefix=['!', '>>', 'feubot '], description="Hi I'm feubot. I'm case sensitive.", formatter = FeubotFormatter())

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



    @bot.event
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')
        #await bot.change_presence(status=discord.Status.idle, activity=game)
        await bot.change_presence(activity=discord.Game(name="Eating some beans."))

    @bot.add_listener
    async def on_command_error(error, ctx):
        if type(error) == commands.CheckFailure:
            pass
        elif type(error) == commands.CommandNotFound:
            pass
        else:
            print(error)#await ctx.channel.send ("ctx.message.channel, error")

###################The Legend
    @bot.command()
    async def donate(ctx):
        """you know it"""
        await ctx.channel.send("https://www.patreon.com/theFEUfund")
        await ctx.channel.send("https://donorbox.org/donate-to-circles")

##################Local

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
                await ctx.channel.send(embed=create_embed(posts, threads, payload))
            except urllib.error.URLError:
                await ctx.channel.send("Error accessing FEU server, please try again later.")

    @bot.command()
    async def UT2(ctx):
        """links ultimate tutorial v2"""
        await ctx.channel.send("https://stackedit.io/viewer#!provider=gist&gistId=084645b0690253600f4aa2a57b76a105&filename=feutv2")

    @bot.command()
    async def reply(ctx):
        """r e p l y s o o n"""
        await ctx.channel.send("reply :soon: :smile:")

    @bot.command()
    async def arch(ctx):
        """do something with arch"""
        direction = random.choice([":arrow_down:", ":arrow_up:", ":arrow_up_down:", ":question:", ":heart:"])
        await ctx.channel.send(direction+" with <:arch_mini:230160993299202068>")

    @bot.command()
    async def goofs(ctx):
        """list goofs"""
        await ctx.channel.send("```"+"\n".join(map(str, os.listdir("./goofs")))+"```")

    @bot.command()
    async def goof(ctx, *args):
        """show goof"""
        requested = args
        gooflist = os.listdir("./goofs")
        if len(requested) != 0:
            for request in requested:
                if request in gooflist:
                    await ctx.channel.send(file=discord.File("./goofs/"+request))
                else:
                    await ctx.channel.send("Use >>goofs to see a list of accepted goofs.")
        else:
            await ctx.channel.send(file=discord.File("./goofs/"+random.choice(gooflist)))

    @bot.command()
    async def erin(ctx):
        """ERIN INTENSIFIES"""
        await ctx.channel.send(file=discord.File("./erinyous.gif"))

    @bot.command()
    async def fury(ctx):
        """2 FAST 2 FURYOUS"""
        await ctx.channel.send("Don't you mean `>>erin`?")

    @bot.command()
    async def doot(ctx):
        """doot doot"""
        await ctx.channel.send("""<:doot:324593825815461889> <:doot:324593825815461889> :trumpet: :trumpet: :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: <:doot:324593825815461889> <:doot:324593825815461889> <:doot:324593825815461889>
    <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: <:doot:324593825815461889> :trumpet:
    <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: <:doot:324593825815461889> :trumpet:
    <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: <:doot:324593825815461889> :trumpet:
    <:doot:324593825815461889> <:doot:324593825815461889> :trumpet: :trumpet: :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: :trumpet: <:doot:324593825815461889> :trumpet: :trumpet: :trumpet: <:doot:324593825815461889> :trumpet:""")

########################Helpful

#    @bot.command()
 #   async def help(ctx):
  #      """Long list of commands"""
   #     await ctx.channel.send("I'm case sensitive, please be gentle.        !donate        !search (question)        !UT2        !reply        !arch        !goofs        !goof (goof.png)        !erin        !fury        !doot        !howtomod        !goldmine        !repository/!repo        !mugs        !hit (n)        !roll (n)        !rollDie/!diceroll (number)        !gotobed        !useyourhead        !drink        !sain        !theband        !whattime        !orbit        !writing        !wtfdyjsamylb\!wtf        !ma___a/!ma???a        !evil (ex)        !colorz        !style        !whois (user)        !createwaifu        !lol        !ea/!eventassembler/!everythingassembler        !casual        !slow        !soa/SOA/SoA        !hard        !brainblast        !ews        !ew (ew.png)        !incredible        !crackers        !hector        !eliwood        !lyn        !spritans        !ree/e/e        !F/!f/!respects        !enough        !creepy        !tethys        !marisa        !lel        !approve        !ok/OK        !uberthink        !awful/!awfuldisplay")


    @bot.command()
    async def report7z(ctx):
        """Report7z reminder"""
        await ctx.channel.send("Please send report7z.")
        await ctx.channel.send("https://dw.ngmansion.xyz/doku.php?id=en:guide:febuildergba:report7z")

    @bot.command(pass_context = True)
    async def mod(ctx, rule_num, *, link):
        """!mod <rule number> <link to objectionable message>"""
        FEU_id = "144670830150811649"
        if ctx.message.guild is None or ctx.message.guild.id == FEU_id:
            await ctx.channel.send(ctx.message.author, "Your request for moderation was successful.")
            if ctx.message.guild is not None:
                await Message.delete(ctx.message)
            mod_channel = self.bot.get_channel("650911156277477377")
            paladins = discord.utils.get(ctx.message.server.roles, id="145992793796378624").mention
            await ctx.channel.send(mod_channel, "%s, moderation request received by user %s: Rule %s, at <%s>." % (paladins, ctx.message.author.name, rule_num, link))
        else:
            await ctx.channel.send("Moderation features are for FEU only.")

    @bot.command()
    async def howtomod(ctx):
        """Gives information on how to use the !mod command."""
        await ctx.channel.send("First, have Developer Mode enabled (Settings -> Appearance -> Developer Mode).")
        await ctx.channel.send("Then, click the `...` by the offending message, and click \"Copy Link\".")
        await ctx.channel.send("Then simple say !mod <n> <link>, where <n> is the rule it violates, and <link> is the pasted link to the message.")
        await ctx.channel.send("If you do not have Developer Mode, you may instead of a link, write a short description of where the infraction took place, and by who.")
        await ctx.channel.send("Note that after requesting moderation, the message requesting moderation will be removed.")


    @bot.command()
    async def goldmine(ctx):
        """everything you ever wanted"""
        embed=discord.Embed(title="Unified FE Hacking Dropbox", url='https://www.dropbox.com/sh/xl73trcck2la799/AAAMdpNSGQWEzYkLEQEiEhGFa?dl=0', description="All the hacking resources you could ever need, in one place", color=0xefba01)
        # embed.set_thumbnail(url='http://i.imgur.com/Bg5NSga.png')
        await ctx.channel.send(embed=embed)


    @bot.command(aliases=["repo"])
    async def repository(ctx):
        """graphics for you"""
        embed=discord.Embed(title="Emblem Anims", url='https://emblem-anims.herokuapp.com/', description="Get your animations here (credits missing on some, check just in case!)", color=0x4286f4)
        await ctx.channel.send(embed=embed)

    @bot.command()
    async def mugs(ctx):
        """Link to image of all GBAFE mugs."""
        await ctx.channel.send("http://doc.feuniverse.us/static/resources/mugs.png")

    @bot.command()
    async def hit(ctx, number, type="2RN"):
        """Convert 2RN/fates hit to actual chance"""
        try:
            num = int(number)
        except ValueError:
            await ctx.channel.send("Specify an integer 0-100")
            return
        if (num < 0) or (num > 100):
            await ctx.channel.send("Specify an integer 0-100")
            return
        if type.upper()=="2RN":
            table = [0.00, 0.03, 0.10, 0.21, 0.36, 0.55, 0.78, 1.05, 1.36, 1.71, 2.10, 2.53, 3.00, 3.51, 4.06, 4.65, 5.28, 5.95, 6.66, 7.41, 8.20, 9.03, 9.90, 10.81, 11.76, 12.75, 13.78, 14.85, 15.96, 17.11, 18.30, 19.53, 20.80, 22.11, 23.46, 24.85, 26.28, 27.75, 29.26, 30.81, 32.40, 34.03, 35.70, 37.41, 39.16, 40.95, 42.78, 44.65, 46.56, 48.51, 50.50, 52.47, 54.40, 56.29, 58.14, 59.95, 61.72, 63.45, 65.14, 66.79, 68.40, 69.97, 71.50, 72.99, 74.44, 75.85, 77.22, 78.55, 79.84, 81.09, 82.30, 83.47, 84.60, 85.69, 86.74, 87.75, 88.72, 89.65, 90.54, 91.39, 92.20, 92.97, 93.70, 94.39, 95.04, 95.65, 96.22, 96.75, 97.24, 97.69, 98.10, 98.47, 98.80, 99.09, 99.34, 99.55, 99.72, 99.85, 99.94, 99.99, 100.00]
        elif type.upper()=="FATES":
            table = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50.5,51.83,53.17,54.5,55.83,57.17,58.5,59.83,61.17,62.5,63.83,65.17,66.5,67.83,69.17,70.5,71.83,73.17,74.5,75.83,77.17,78.5,79.83,81.17,82.5,83.83,85.12,86.35,87.53,88.66,89.73,90.75,91.72,92.63,93.49,94.3,95.05,95.75,96.4,96.99,97.53,98.02,98.45,98.83,99.16,99.43,99.65,99.82,99.93,99.99,100]
        else:
            await ctx.channel.send("Valid types are 2RN, Fates")
            return
        await ctx.channel.send(str(table[num]))

    @bot.command()
    async def roll(ctx, number, type="2RN"):
        """rolls hit or miss (e.g. >>hit 50 1rn/2rn[default]/fates)"""
        try:
            num = int(number)
        except ValueError:
            await ctx.channel.send("Specify an integer 0-100")
            return
        if (num < 0) or (num > 100):
            await ctx.channel.send("Specify an integer 0-100")
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
            await ctx.channel.send("Valid types are 1RN, 2RN, Fates")
            return
        if rolled <= num: await ctx.channel.send("HIT (%d)" % rolled)
        else: await ctx.channel.send("MISS (%d)" % rolled)

    @bot.command(name="diceroll")
    async def rollDie(ctx, n : int):
        if n <= 0:
            await ctx.channel.send("Specify a positive integer.")
            return
        res = random.randrange(n) + 1
        await ctx.channel.send(str(res))


########################Memes


    @bot.command()
    async def familyfriendly (ctx):
        """Pooh the berserker"""
        await ctx.channel.send(file=discord.File("./familyfriendly.png"))                                     
    
    @bot.command()
    async def cattheft (ctx):
        """gimme"""
        await ctx.channel.send("It’s not really theft. It’s unsolicited `cat taking`. Both ways. It’s the highest form of admiration and appreciation. Besides, I needn’t a lecture. I’m quite aware, I’ve been around a long time. On and off from the beginning, or close to it. You know how many `cats` I haven’t been able to `steal` due to these rules? I’m sorry your infinitely replicable series of `cats` get used to make other things when you’re not lording over every `cat` in circulation. My deepest apologies. If you weren’t so good, at times, I’d be more blunt and heavy handed about this.")

    @bot.command()
    async def credit (ctx):
        """huwhwa"""
        await ctx.channel.send("Yes, I do. I contacted the person who submitted/made it online. Right, of course, I'm not going to go stealing others' hard work, that's just wrong. What do you mean? I'm not trying to force people to help me, if that's what you're saying. That's why I said if anyone wants to help me, that'd be really appreciated. If I was forcing people to do it, I'd have said it with a threat, if that makes sense.")


    @bot.command()
    async def ears (ctx):
        """wtf"""
        await ctx.channel.send(file=discord.File("./ears.png"))

    @bot.command()
    async def gotonap(ctx):
        "naptime"
        await ctx.channel.send(file=discord.File("./gotonap.png"))

    @bot.command()
    async def hackradd(ctx):
        "is it tho?"
        await ctx.channel.send(file=discord.File("./hackradd.png"))

    @bot.command()
    async def zanesjw(ctx):
        "the best sjw"
        await ctx.channel.send(file=discord.File("./zanesjw.png"))

    @bot.command()
    async def yeszane(ctx):
        "skeleyes"
        await ctx.channel.send(file=discord.File("./yeszane.jpg"))

    @bot.command()
    async def zane(ctx):
        "I agree with the skeleton"
        await ctx.channel.send(file=discord.File("./zane.png"))

    @bot.command()
    async def topkek(ctx):
        "Off the top"
        await ctx.channel.send(file=discord.File("./topkek.jpg"))

    @bot.command()
    async def nyeh(ctx):
        """skelepirate"""
        await ctx.channel.send(file=discord.File("./nyeh.png"))

    @bot.command()
    async def hisworld(ctx):
        """sonic ememememee"""
        await ctx.channel.send("https://www.youtube.com/watch?v=d2tdSiQAF20")

    @bot.command()
    async def work (ctx):
        """Gosh darn delinquents"""
        await ctx.channel.send("Get back to work you maggots!!!")

    @bot.command()
    async def keriku (ctx):
        """Kelikringe"""
        await ctx.channel.send("https://cdn.discordapp.com/attachments/261347653084905482/511231047254409217/Kookil_ket.webm")

    @bot.command()
    async def klek (ctx):
        """Kelik"""
        await ctx.channel.send("`I invoke the wrath of`")
        await ctx.channel.send("`I invoke the wrath of`")
        await ctx.channel.send("`Grant me the power to rid`")
        await ctx.channel.send("`of these corrupt souls...`")

    @bot.command()
    async def thisdivinelightning (ctx):
        """The holy thunder"""
        await ctx.channel.send("shall pierce the skies!")

    @bot.command()
    async def frenchzane (ctx):
        """Zane's truest form"""
        await ctx.channel.send(file=discord.File("./paintmelikeoneofyourfrenchgirls.png"))

    @bot.command()
    async def wav2egg (ctx):
        """the big oof"""
        await ctx.channel.send(file=discord.File("./wav2egg.png"))

    @bot.command()
    async def gotobed (ctx):
        """Listen to your doctors"""
        await ctx.channel.send(file=discord.File("./gotobed.png"))

    @bot.command(aliases=["head"])
    async def useyourhead (ctx):
        """Way to use your head, Ephraim."""
        await ctx.channel.send(file=discord.File("./head.gif"))

    @bot.command(aliases=["ketchup"])
    async def drink (ctx):
        """But is it a smoothie??"""
        await ctx.channel.send(file=discord.File("./Cheers.gif"))

    @bot.command()
    async def sain (ctx):
        """Horny horseman"""
        await ctx.channel.send(file=discord.File("./Sain.jpeg"))

    @bot.command(aliases=["band"])
    async def theband (ctx):
        """I doubt the titanic was this dedicated"""
        await ctx.channel.send(file=discord.File("./the band.gif"))

    @bot.command()
    async def whattime(ctx):
        """tells the time"""
        await ctx.channel.send("`it's tiki time`")
        # await asyncio.sleep(1)
        await ctx.channel.send(file=discord.File("tiki.gif"))

    @bot.command()
    async def orbit(ctx):
        """my tiki's"""
        await ctx.channel.send(file=discord.File("Tikis_in_orbit.png"))

    @bot.command()
    async def writing(ctx):
        """get it in writing. in blood."""
        await ctx.channel.send(file=discord.File("Pelleass_Blood_Pact.png"))

    @bot.command(name="wtf")
    async def wtfdyjfsamylb(ctx):
        """what the fuck did you just fucking say about me you little bitch"""
        await ctx.channel.send("""```
What the fuck did you just fucking say about me, you little bitch? I’ll have you know I graduated top of my class in the FE University, and I’ve been involved in numerous secret raids on Serenes Forest, and I have over 300 confirmed hacks. I am trained in donating to hex and I’m the top debugger in the entire FE Shrine. You are nothing to me but just another breakpoint. I will wipe you the fuck out with precision the likes of which has never been seen before on an ARMv7TDMI, mark my fucking words. You think you can get away with saying that shit to me over the Internet? Think again, fucker. As we speak I am contacting my secret network of backups across the ROM and your link register is being traced right now so you better prepare for the screech, fleshling. The death screech that wipes out the pathetic little thing you call your reskin. You’re fucking dead, kid. I can be anywhere, anytime, and I can crash your rom in over seven hundred ways, and that’s just with FEditor. Not only am I extensively trained in Nightmare, but I have access to the entire arsenal of the Unified FE Hacking Doc and I will use it to its full extent to wipe your miserable map sprite off the face of Magvel, you little shit. If only you could have known what unholy retribution your little “clever” comment was about to bring down upon you, maybe you would have held your fucking tongue. But you couldn’t, you didn’t, and now you’re paying the price, you goddamn idiot. I will shit Erin all over you and you will drown in it. You’re fucking dead, kiddo.
```""")

    @bot.command(name="ma???a")
    async def ma___a(ctx):
        """what IS her name anyway"""
        letters = [x for x in "abcdefghijklmnopqrstuvwyxz"]
        consonants = [x for x in "bcdfghjklmnpqrstvwxz"]
        vowels = [x for x in "aeiouy"]
        infix = random.choice(consonants) + random.choice(letters) + random.choice(vowels)
        await ctx.channel.send("I think you mean Ma"+infix+"a!")

    @bot.command()
    async def evil(ctx, *args):
        """Sub-humans."""
        if len(args) > 0:
            thing = ' '.join(args)
            plural = thing[-1] == 's' #TODO: use inflect
            formatString = '''```\n{1} {0} evil.\n{1} {0} the enemy.\n{1} must be eradicated.```'''
            verb = "are" if plural else "is"
            await ctx.channel.send(formatString.format(verb, thing))
        else:
            await ctx.channel.send("You gotta tell me **what's** evil!")


    @bot.command()
    async def colorz(ctx):
        """do something with colorz"""
        direction = random.choice([":arrow_down:", ":arrow_up:"])
        await ctx.channel.send(direction+" with <:colorz:230159530158194688>")


    @bot.command()
    async def style(ctx):
        """if my style gets in your way"""
        img = random.choice(["styleRD.gif", "stylePoR.jpeg"])
        await ctx.channel.send(file=discord.File(img))


    @bot.command()
    async def whois(ctx,*args):
        """roy is our boy"""
        if len(args) > 0:
            lord = ' '.join(args)
            if (lord.lower() in ['circles','circleseverywhere']):
                await ctx.channel.send(lord + " is my dad")
                return
            elif (lord.lower() == 'feditor'):
                await ctx.channel.send("`" + lord + " a shit`")
                return
            elif (lord.lower() == 'feubot'):
                await ctx.channel.send("That's me, silly!")
                return
            elif (lord.lower() == 'ea'):
                await ctx.channel.send("`" + lord + " is our bae`")
                return
            elif (lord.lower() in ['bm', 'blackmage', 'black mage']):
                await ctx.channel.send(file=discord.File("BMis.gif"))
                return
            elif lord[0].lower() in 'bcdfghjklmnpqrstvwxz':
                blord = 'b'+lord[1:]
            else:
                blord = 'b'+lord
            await ctx.channel.send(lord + " is our " + blord)

    @bot.command()
    async def createwaifu(ctx,*args):
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
            "<:dootthunk:339479700147798016>",
            "<:doot:324593825815461889>",
            "<:donate:230166446146191362>",
            "<:doc:280527122802540544>",
            "<:colorz:230159530158194688>",
            "<:circles:238177111418863617>",
            "<:celica:272027128231362571>",
            "<:BBQ:230169373694885888>",
            "<:arch_mini:230160993299202068>",
            "<:camthumb:307559627573428224>",
            "<:dat:292422389197701121>",
            "<:thighs:294965155819683840>"]
        if len(args) > 0: head = ' '.join(args)
        else: head = random.choice(heads)
        await ctx.channel.send(head + """
<:personality:385616854451748864>
<:thighs:294965155819683840>""")


    @bot.command(aliases=["(lol"])
    async def lol(ctx):
        """(lol"""
        flip = random.choice([0,1])
        if flip==1: await ctx.channel.send(file=discord.File("./Water_lol.png"))
        else: await ctx.channel.send(file=discord.File("./Water_lol2.png"))

    @bot.command(aliases=["eventassembler", "everythingassembler"])
    async def ea(ctx):
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
        await ctx.channel.send(everythingassemblerstring)

    @bot.command()
    async def casual(ctx):
        """just play phoenix"""
        barflist = os.listdir("./casual")
        await ctx.channel.send(file=discord.File("./casual/"+random.choice(barflist)))


    @bot.command()
    async def slow(ctx):
        """It's what I ain't."""
        await ctx.channel.send(file=discord.File("./slow.png"))


    @bot.command(aliases=["SOA", 'SoA'])
    async def soa(ctx):
        """there's your problem"""
        await ctx.channel.send(file=discord.File("./SoA.png"))

    @bot.command()
    async def hard(ctx):
        """HARD"""
        await ctx.channel.send(file=discord.File("./hard.png"))



########################Reactions


    @bot.command()
    async def brainblast(ctx):
        """Big Brain Explosion"""
        await ctx.channel.send(file=discord.File("./Thunksplosion.gif"))

    @bot.command()
    async def ews(ctx):
        """disgusting list"""
        filenameslist = [os.path.splitext(f)[0] for f in os.listdir("./disgusting")]
        await ctx.channel.send("```"+"\n".join(map(str, filenameslist))+"```")

    @bot.command()
    async def ew(ctx,*args):
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
                        await ctx.channel.send(file=discord.File("./disgusting/"+ewlist[request_file]))
                if not found:
                    await ctx.channel.send("Use >>ews to see a list of accepted names.")
        else:
            await ctx.channel.send(file=discord.File("./disgusting/"+random.choice([a for a in ewlist.values()])))

    @bot.command(aliases=["incredible"])
    async def fuckingincredible(ctx):###
        """fuckingincredible.png"""
        await ctx.channel.send("http://i.imgur.com/yt4hXhJ.png")

    @bot.command()
    async def crackers(ctx):
        """jumping boat monkeys!"""###
        await ctx.channel.send(file=discord.File("./Holy_crackers.png"))

    @bot.command()
    async def hector(ctx):
        """judges you"""
        await ctx.channel.send(file=discord.File("./hectorpc.png"))

    @bot.command()
    async def eliwood(ctx):
        """:("""
        await ctx.channel.send(file=discord.File("./eliwoodpc.jpg"))

    @bot.command()
    async def lyn(ctx):
        """>:("""
        await ctx.channel.send(file=discord.File("./lynpc.png"))

    @bot.command()
    async def spritans(ctx):
        """REEE"""
        await ctx.channel.send("muh")
        await asyncio.sleep(1)
        await ctx.channel.send("SPRITANS")
        await asyncio.sleep(2)
        await ctx.channel.send("***REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE***")


    @bot.command(aliases=["reeee", 'ree'])
    async def reee(ctx):
        """REEEEEEEEEEEEEEEEEEE"""
        action = random.choice([1,2])
        if action==1:
            msg = "*REEE*"
            await asyncio.sleep(0.5)
            await asyncio.sleep(0.25)
            await ctx.channel.send(msg + "                   **REEEEEEEEEEE**                  ")
            await asyncio.sleep(0.5)
            await ctx.channel.send("***REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE***")
        else:
            await ctx.channel.send(file=discord.File("./reee.gif"))

    @bot.command(aliases=["f", 'respects'])
    async def F(ctx):
        """Press F to pay respects."""
        await ctx.channel.send(file=discord.File("./respects.jpeg"))

    @bot.command()
    async def enough(ctx):
        """you wouldn't like me when i'm angry"""
        await ctx.channel.send(file=discord.File("./enough.png"))

    @bot.command()
    async def creepy(ctx):
        """stay away"""
        await ctx.channel.send(file=discord.File("./creepy.png"))

    @bot.command()
    async def tethys(ctx):
        """dancer think"""
        await ctx.channel.send(file=discord.File("./tethys.png"))

    @bot.command()
    async def marisa(ctx):
        """u srs"""
        await ctx.channel.send(file=discord.File("./marisa.png"))

    @bot.command()
    async def lel(ctx):
        """lel"""
        img=random.choice(["./lel.png","./lel2.png"])
        await ctx.channel.send(file=discord.File(img))

    @bot.command(pass_context=True, hidden=True)
    async def approve(ctx):
        pid = str(ctx.message.author.id)
        if pid == "171863408822452224":
            await ctx.channel.send(file=discord.File('./approved.png'))
        elif pid == '59462571601702912':
            await ctx.channel.send(file=discord.File('./Letha_Seal_of_Approval.png'))
        else:
            await ctx.channel.send(file=discord.File('./FEU_Seal.png'))

    @bot.command(aliases=["OK"])
    async def ok(ctx):
        """ok"""
        await ctx.channel.send(file=discord.File("./ok.png"))

    @bot.command()
    async def uberthink(ctx):
        """ðŸ¤”"""
        await ctx.channel.send(file=discord.File("./uberthink.gif"))

    @bot.command(aliases=["awfuldisplay"])
    async def awful(ctx):
        """for when someone posts cringe"""
        await ctx.channel.send(file=discord.File("./awful.jpg"))



####################################
    bot.reload = lambda: setupBot(bot)
    #setupBot(bot)
    bot.run(TOKEN)
    token = os.environ.get('TOKEN', default=None)

    if token is None:
        token = open('./token').read().replace('\n','')
