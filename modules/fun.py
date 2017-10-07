import checks
import aiohttp
import json


class Fun:

    def __init__(self,
                 bot):
        self.bot = bot

    @checks.command()
    async def chucknorris(self,
                          ctx,
                          args):
        """Chuck norris jokes"""
        url = "https://api.chucknorris.io/jokes/random"
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        async with aiohttp.get(url) as f:
            result = await f.read()
        jokeDic = result.decode('utf-8')
        joke = json.loads(jokeDic)['value']
        ctx.send(joke,
                 payload={
                     'chucknorris': 'chucknorris'
                 })


def setup(bot):
    bot.addModule(Fun(bot))
