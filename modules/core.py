import asyncio
import exceptions

from datetime import datetime, timedelta

import checks


class Core:

    def __init__(self, bot):
        self.bot = bot

    @checks.command()
    async def smalltest(self, ctx, args):
        ctx.send("FINALLY IT WORKS!")

    @checks.command()
    async def waiter(self, ctx, args):
        ctx.send("Time to sleep.")
        await asyncio.sleep(5)
        ctx.send("Done sleeping!")

    @checks.command()
    async def tic(self,
                  ctx,
                  args):
        ctx.send("Tac",
                 payload={
                     'same': 'lmao'
                 })

    @checks.command()
    async def time(self,
                   ctx,
                   args):
        temp = datetime.utcnow()
        now = temp + timedelta(hours=2)
        currentTime = '{:%d/%m/%Y %H:%M:%S}'.format(now)
        ctx.send(currentTime)

    @checks.command()
    def google(self,
               ctx,
               args):
        """Google something"""
        if not args:
            raise exceptions.InvalidArguments
            return
        s = "+".join(args)
        msg = "https://www.google.com/?q={s}#newwindow=1&q={s}".format(s=s)
        ctx.send(msg)


def setup(bot):
    bot.addModule(Core(bot))
