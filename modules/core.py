import asyncio
import checks


class Core:

    def __init__(self, bot):
        self.bot = bot

    @checks.command()
    async def smalltest(self, ctx, args):
        ctx.send("FINALLY IT WORKS!")

    async def dontwork(self, ctx, args):
        ctx.send("pls don't work")

    @checks.command()
    async def waiter(self, ctx, args):
        ctx.send("Time to sleep.")
        await asyncio.sleep(5)
        ctx.send("Done sleeping!")


def setup(bot):
    bot.addModule(Core(bot))
