from sendMessage import Send


class Message:

    def __init__(self,
                 author,
                 message,
                 timestamp,
                 recipient):
        """
        Process the message and split it into arguments and attributes.
        Example:
            message = 'google something please'
            com = 'google'
            args = ['something', 'please']
        """
        self.author = author
        try:
            self.quick_replies = message['quick_reply']
        except KeyError:
            pass
        self.content = message['text']
        self.time = timestamp
        self.recipient = recipient
        self.command = self.get_command()
        self.arguments = self.get_args()

    def get_command(self):
        """Get the command used"""
        com = self.content.lower().split(" ")[0]
        return com

    def get_args(self):
        """Get arguments parsed"""
        msg_list = self.content.lower().split(" ")
        if len(msg_list) > 1:
            args = msg_list[1:]
        else:
            args = None
        return args


class Context:
    """The context class"""

    def __init__(self,
                 message):
        self.message = message
        self.send = Send(message.author).send
        self.say = self.send


class Command:
    """The command class"""

    def __init__(self,
                 func,
                 module,
                 name):
        self.run = func
        self.name = name
        self.module = type(module).__name__


class Colours:

    def __init__(self):
        self._header = '\033[95m'
        self._blue = '\033[94m'
        self._green = '\033[92m'
        self._warning = '\033[93m'
        self._fail = '\033[91m'
        self._bold = '\033[1m'
        self._underline = '\033[4m'
        self._end = '\033[0m'

    def end(self, text):
        return text + self._end

    def orange(self, text):
        return self.end(self._header + text)

    def blue(self, text):
        return self.end(self._blue + text)

    def green(self, text):
        return self.end(self._green + text)

    def yellow(self, text):
        return self.end(self._warning + text)

    def red(self, text):
        return self.end(self._fail + text)

    def bold(self, text):
        return self.end(self._bold + text)

    def underline(self, text):
        return self.end(self._underline + text)

"""
class User:
    def __init__(self,
                 name=None,
                 id):
        #self.name =
        pass
"""
