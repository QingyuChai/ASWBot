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
        self.quick_replies = message['quick_reply']
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
    def __init__(self,
                 message):
        self.message = message
        self.send = Send(message.author).send
        self.say = self.send
