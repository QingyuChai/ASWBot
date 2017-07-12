import checks
import json
from contentTypes import Colours as c


class Help:

    def __init__(self, bot):
        self.bot = bot
        self.c = c()

    @checks.command(name='help')
    async def _help(self, ctx, args):
        """A simple help command"""

        payload = {
            'chucknorris': 'chucknorris',
            'time': 'time'
        }

        commandDic = self.bot.commands
        moduleDic = self.bot.modules

        moduleList = [m for m in moduleDic]
        commandList = [c for c in commandDic]

        helpDic = {}

        for modName, modObject in moduleDic.items():
            helpDic[modName] = []

            for comName, comObject in commandDic.items():
                if comObject.module == modName:
                    helpDic[modName].append(comName)

        # The below is just to check the dic
        # print(self.c.orange(json.dumps(helpDic, indent=4, sort_keys=True)))

        msg = 8 * '-' + "\n"

        for mod, comList in helpDic.items():
            msg += mod.upper() + "\n"
            msg += " | ".join(comList) + "\n"
            msg += 8 * '-' + "\n"

        ctx.send(msg,
                 payload=payload)


def setup(bot):
    bot.addModule(Help(bot))
