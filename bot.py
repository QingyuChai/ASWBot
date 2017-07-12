import json
import asyncio
import websockets
import rethinkdb as r
import importlib
import inspect
from types import *

from pydispatch import dispatcher
import checks
import exceptions
import contentTypes

# erase the modules file
"""
with open('modules.json', 'w') as f:
    f.write(json.dumps({
        'modules': []
    },
        indent=4,
        sort_keys=True)
    )
"""

__version__ = "2.0.0"


class Bot:

    def __init__(self):
        # Initialize prints, so we know what is going on
        print("\n\n\n\n=====================================")
        self.id = "413050579062125"
        print("[+] Connecting to Database...")
        self.initDatabase()
        print("[+] Loading modules...")
        self.initModules()
        print("[+] Ready to accept commands!")
        print("=====================================")

    def initModules(self):
        self.modules = {}
        self.commands = {}
        moduleList = json.loads(open('modules.json', 'r').read())["modules"]
        for module in moduleList:
            tempMod = importlib.import_module('modules.{}'.format(module))
            tempMod.setup(self)

    def initDatabase(self):
        self.c = r.connect()
        self.c.use("Facebook")

    def addModule(self,
                  module):
        self.modules[type(module).__name__] = module
        myIter = inspect.getmembers(module, predicate=inspect.ismethod)
        # print(myIter)
        for myMethod in myIter:
            methodFunc = myMethod[1]
            methodName = methodFunc.__name__.lower()
            if hasattr(methodFunc, "is_command"):
                # do something with the method and class
                tempCom = contentTypes.Command(func=methodFunc,
                                               name=methodName,
                                               module=module)
                self.commands[tempCom.name] = tempCom

        # print(self.modules)
        # for command in

    async def onMessage(self,
                        message):
        """
        Event on_message:
            For every message sent, this function is called to process the
            message received.
        """
        context = contentTypes.Context(message=message)
        try:
            # We want it to respond if it replies with a command that does not
            # exist or is not available
            print("[+] Command \"{}\" accepted... Checking "
                  "for validity.".format(context.message.command))
            if context.message.command not in self.commands:
                raise exceptions.InvalidCommand
            await self.runCommand(ctx=context)
            print("[+] Command valid, processing now...")
        except exceptions.InvalidCommand:
            # Command doesn't exist
            print("[-] Command '{}' doesn't exist."
                  .format(context.message.command))
            context.send("Sorry, invalid command.")
        except exceptions.InvalidArguments:
            # Invalid command arguments passed
            print("[-] Command '{}' was passed with invalid arguments."
                  .format(context.message.command))
            context.send("Sorry, invalid arguments.")
        except Exception as e:
            # Unexpected error
            print("[-] Unexpected Error occured. Error logs here:\n\n" + e)
            context.send("Sorry, an unexpected error has occured.")

    async def runCommand(self,
                         ctx):
        command = ctx.message.command

        # ctx.args has to be rewritten with functools
        await self.commands[command].run(ctx, ctx.message.arguments)

    async def listen(self, socket, path):
        """
        This is the change dictionary that is returned
        {
            'sender' : {
                'id' : foo
            },
            'timestamp' : foo,
            recipient : {
                'id' : foo
            },
            'message' : foo

        }
        """

        response = await socket.recv()
        try:
            initial_request = json.loads(response.replace("'", "\""))
        except:
            return

        author = initial_request['sender']['id']
        timestamp = initial_request['timestamp']
        recipient = initial_request['recipient']['id']
        message = initial_request['message']

        Message = contentTypes.Message(author=author,
                                       message=message,
                                       timestamp=timestamp,
                                       recipient=recipient)

        if Message.author == self.id:
            # We don't want the bot to answer it's own messages
            return

        await self.onMessage(message=Message)


def main(loop):
    messageListener = websockets.serve(Bot().listen, 'localhost', 1111)
    loop.run_until_complete(messageListener)
    loop.run_forever()


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        main(loop)
    except KeyboardInterrupt:
        print("[-] Application exited due to manual keyboard input.")
