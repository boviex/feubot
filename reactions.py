import discord
from discord.ext import commands as bot
import os, random, re, asyncio

class Reactions(bot.Cog):
    """memes but not"""

    def __init__(self, bot):
        self.bot = bot

    @bot.command()
    async def ews(self, ctx):
        """disgusting list"""
        filenameslist = [os.path.splitext(f)[0] for f in os.listdir("./disgusting")]
        await ctx.send("```"+"\n".join(map(str, filenameslist))+"```")

    @bot.command()
    async def ew(self, ctx,*args):
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
                        await ctx.send(file=discord.File("./disgusting/"+ewlist[request_file]))
                if not found:
                    await ctx.send("Use >>ews to see a list of accepted names.")
        else:
            await ctx.send(file=discord.File("./disgusting/"+random.choice([a for a in ewlist.values()])))

    @bot.command()
    async def fuckingincredible(self, ctx, aliases=["incredible"]):
        """fuckingincredible.png"""
        await ctx.send("http://i.imgur.com/yt4hXhJ.png")

    @bot.command()
    async def crackers(self, ctx):
        """jumping boat monkeys!"""
        await ctx.send(file=discord.File("./Holy_crackers.png"))

    @bot.command()
    async def hector(self, ctx):
        """judges you"""
        await ctx.send(file=discord.File("./hectorpc.png"))

    @bot.command()
    async def eliwood(self, ctx):
        """:("""
        await ctx.send(file=discord.File("./eliwoodpc.jpg"))

    @bot.command()
    async def lyn(self, ctx):
        """>:("""
        await ctx.send(file=discord.File("./lynpc.png"))

    @bot.command()
    async def spritans(self, ctx):
        """REEE"""
        await ctx.send("muh")
        await asyncio.sleep(1)
        await ctx.send("SPRITANS")
        await asyncio.sleep(2)
        await ctx.send("***REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE***")


    @bot.command()
    async def reee(self, ctx):
        """REEEEEEEEEEEEEEEEEEE"""
        action = random.choice([1,2])
        if action==1:
            msg = await ctx.send("*REEE*")
            await asyncio.sleep(0.5)
            for i in range(1, random.randint(5,10)):
                await asyncio.sleep(0.25)
                await msg.edit(content = "**REEE" + "E"*i + "**")
            await asyncio.sleep(0.25)
            await msg.edit(content = "***REEE" + "E"*(i+1) + "***")
        else:
            await ctx.send(file=discord.File("./reee.gif"))           

    @bot.command()
    async def F(self, ctx):
        """Press F to pay respects."""
        await ctx.send(file=discord.File("./respects.jpeg"))

    @bot.command()
    async def enough(self, ctx):
        """you wouldn't like me when i'm angry"""
        await ctx.send(file=discord.File("./enough.png"))

    @bot.command()
    async def creepy(self, ctx):
        """stay away"""
        await ctx.send(file=discord.File("./creepy.png"))

    @bot.command()
    async def tethys(self, ctx):
        """dancer think"""
        await ctx.send(file=discord.File("./tethys.png"))

    @bot.command()
    async def marisa(self, ctx):
        """u srs"""
        await ctx.send(file=discord.File("./marisa.png"))

    @bot.command()
    async def lel(self, ctx):
        """lel"""
        img=random.choice(["./lel.png","./lel2.png"])
        await ctx.send(file=discord.File(img))

    @bot.command()
    async def approve(self, ctx, pass_context=True, hidden=True):
        pid = str(ctx.message.author.id)
        if pid == 171863408822452224:
            await ctx.send(file=discord.File('./approved.png'))
        elif pid == '59462571601702912':
            await ctx.send(file=discord.File('./Letha_Seal_of_Approval.png'))    
        else:
            await ctx.send(file=discord.File('./FEU_Seal.png'))

    @bot.command()
    async def ok(self, ctx, aliases=["OK"]):
        """ok"""
        await ctx.send(file=discord.File("./ok.png"))

    @bot.command()
    async def uberthink(self, ctx):
        """🤔"""
        await ctx.send(file=discord.File("./uberthink.gif"))
		
    @bot.command()
    async def awful(self, ctx, aliases=["awfuldisplay"]):
        """for when someone posts cringe"""
        await ctx.send(file=discord.File("./awful.jpg"))

async def setup(bot):
    await bot.add_cog(Reactions(bot))
