
from time import time
from functools import reduce

import discord
from discord.ext import commands as bot
from other import developerIDs

_TIMEOUT = 60

_cache = None

class DeletedCache(object):
    __slots__ = ['channels']

    def insert(self, msg):
        reqt = time()
        key = msg.channel.id
        if key not in self.channels:
            self.channels[key] = [(msg, reqt)]
        else:
            self.channels[key].append((msg, reqt))
            self._prune(key, reqt)

    def last(self, chn, n, name=None):
        if name and len(name)>4: name = name[3:-1] #remove the borders on the id.
        reqt = time()
        self._prune(chn.id, reqt)
        if chn.id not in self.channels: return None
        s = [(msg, ts) for msg, ts in self.channels[chn.id]
                if name is None or msg.author.id == name]
        if not s: return None

        self.channels[chn.id] = [m for m in self.channels[chn.id] if m not in s] #remove the messages we're undeleting.
        return [x[0] for x in s]
        #n = len(s)
        #result = (("%s deleted %d message(s) within the last minute:\n"
        #            % (name,n))
        #        if name is not None
        #        else ("%d deleted message(s) within the last minute:\n" % n))
        #return result + '```' + '\n'.join(m.content for m in s) + '```'

    def __init__(self):
        self.channels = dict()

    def _prune(self, key, reqt):
        if key not in self.channels: return
        self.channels[key] = [
            (msg, ts) for msg, ts in self.channels[key] if reqt-ts <= _TIMEOUT
        ]
        super().__init__()

undeleterPred = lambda ctx: not ctx.message.channel.is_private and discord.utils.get(ctx.message.author.roles, name="Undeleter") is not None
manageMessagePred = lambda ctx: getattr(ctx.message.channel.permissions_for(ctx.message.author), 'manage_messages', None) == True

class UndeleteCog(object):
    AUTHOR_FORMAT = '{author} said:\n```\n{content}```\n'
    NO_AUTHOR_FORMAT ='```\n{content}```\n'
    __slots__ = ['bot']

    @bot.command(pass_context=True, hidden=True)
    @bot.check(lambda ctx: type(ctx.message.author) is discord.Member)
    @bot.check(lambda ctx: undeleterPred(ctx) or manageMessagePred(ctx) or ctx.message.author in developerIDs)
    async def undelete(self, ctx, n=1, name=None):
        msg = ctx.message
        if n < 1: return
        result = _cache.last(msg.channel, n, name)
        if result is not None:
            FORMAT = self.AUTHOR_FORMAT if not name else self.NO_AUTHOR_FORMAT
            await self.bot.say(
                ('{} deleted message(s) by {} within the last minute:\n'.format(len(result), name) if name else
                    '{} deleted message(s) within the last minute:\n'.format(len(result))) +
                reduce(lambda acc, e: acc+e,
                [FORMAT.format(author=msg.author, content=msg.content) for msg in result]
                , "")
                )
        else:
            await self.bot.say(
                'No messages deleted ' +
                ('by %s ' % name if name is not None else '') +
                'within the last minute')

    def __init__(self, bot):
        global _cache
        _cache = DeletedCache()
        self.bot = bot
        async def undeleteError(self, error, ctx):
            await self.bot.send_message(ctx.message.channel, 'You do not have undelete permissions.')
        self.undelete.error(undeleteError)

async def on_message_delete(msg):
    _cache.insert(msg)

def setup(bot):
    await bot.add_cog(UndeleteCog(bot))
    bot.event(on_message_delete)
