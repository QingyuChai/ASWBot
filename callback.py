import sys
import inspect
from datetime import datetime, timedelta
from random import randint as rand
import urllib.request
import json
from random import randint as rand

import importlib
import checks
from send_message import SendMessage

__version__ = "1.0.2"
__doc__ = """
Message processing for the Facebook bot
"""

users = {
    '1527766087257924':'Sven',
    '1870357256323127':'Didi',
    '1359200367505633':'SoYee'
}

modules = [
    'test'
]

"""
# isinstance(x, function):
# to get the type of a function
def dummy():
    pass

function = type(dummy)
"""


class Main:
    """Process what commands it should run"""

    def __init__(self,
                 message,
                 user_id):
        """initialize"""
        self.commands = ['hi',
                         'chucknorris',
                         'time',
                         'google',
                         'example',
                         'reply']
        self.message = message
        self.user_id = user_id
        self.send = SendMessage(self.user_id).send
        self.on_message()

    def run(self,
            com,
            args):
        """Run commands"""

        com = com.lower()

        @checks.command
        def hi(args):
            """nothing much"""
            self.send('Hi')

        @checks.command
        def hello(args):
            self.send("how are you doing")

        @checks.command
        def hey(args):
            hi(args)

        @checks.command
        def chucknorris(args):
            """Chuck norris jokes"""
            url = "https://api.chucknorris.io/jokes/random"
            req = urllib.request.Request(url, headers={
                'User-Agent': 'Mozilla/5.0'
            })

            f = urllib.request.urlopen(req).read().decode('utf-8')
            joke = json.loads(f)['value']
            self.send(joke)

        @checks.command
        def time(args):
            """Get current time"""
            temp = datetime.utcnow()
            now = temp + timedelta(hours=2)
            Y = now.year
            M = now.month
            D = now.day
            h = now.hour
            m = now.minute
            s = now.second
            dmy = "{D}/{M}/{Y} ".format(Y=Y,
                                        M=M,
                                        D=D)
            hms = "{h}:{m}:{s}".format(h=h,
                                       m=m,
                                       s=s)
            msg = dmy + hms
            self.send(msg)

        @checks.command
        def google(args):
            """Google something"""
            if not args:
                raise TypeError
            s = "+".join(args.split(" "))
            msg = "https://www.google.com/?q={s}#newwindow=1&q={s}".format(s=s)
            self.send(msg)

        @checks.command
        def example(args):
            """Example command"""
            # You want the 2 lines below IF you want to user to put in arguments,
            # such as "today", or "23"
            if not args:
                raise TypeError
            msg = "Whatever you want as your reply"
            self.send(msg)

        @checks.command
        def reply(args):
            """Reply with your current message"""

            if not args:
                raise TypeError

            msg = " ".join(args)
            self.send(msg)

        print("Command : " + com)
        eval("{}({})".format(com,
                               args))

    def on_message(self):
        """Triggered every time a message is sent"""

        msg = self.message

        if msg.lower().startswith("how are you doing"):
            self.send("Doing good, thanks!")
            return
        elif msg.lower().startswith("tic"):
            self.send("Tac")
            return

        sep = msg.split(" ")
        com = sep[0].lower()

        if len(sep) > 1:
            args = sep[1:]
            clean_args = ", ".join(["'{}'".format(arg) for arg in args])
        else:
            clean_args = False

        self.process_message(com=com,
                             args=clean_args)

    def process_message(self,
                        com,
                        args):
        """Process the arguments"""
        try:
            self.run(com, args)
        except TypeError as e:
            self.send("Invalid arguments for: {com}".format(com=com))
        except Exception as e:
            print(e)
            self.send("Error. Command not found.")
