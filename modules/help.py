import checks


class Help:

    def __init__(self, bot):
        self.bot = bot

    @checks.command(name='help')
    async def _help(self, ctx, args):
        ctx.send("no halp for u")
        print(self.bot.commands)
        print(self.bot.modules)


def setup(bot):
    bot.addModule(Help(bot))
