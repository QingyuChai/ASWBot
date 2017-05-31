import json
from types import *

from pydispatch import dispatcher
import exceptions
import contentTypes
import rethinkdb as r

# erase the modules file
with open('modules.json', 'w') as f:
    f.write(json.dumps({
        'modules' : []
    },
                       indent=4,
                       sort_keys=True)
            )

__version__ = "2.0.0"

class Bot:
    def __init__(self):
        # Initialize prints, so we know what is going on
        print("\n\n\n\n=====================================")
        self.id = "413050579062125"
        print("[+] Connecting to Database...")
        self.c = r.connect()
        self.c.use("Facebook")
        print("[+] Loading modules...")
        import commands
        self.modules = json.loads(open('modules.json','r').read())['modules']
        print("[+] Initalizing listeners...")
        self.initialize_listeners()
        print("[+] Listening to input...")
        self.listen()

    def on_message(self, message):
        """
        Event on_message:
            For every message sent, this function is called to process the
            message received.
        """
        if message.author == self.id:
            # We don't want the bot to answer it's own messages
            return
        context = contentTypes.Context(message=message)
        print("[+] Message received. Content:\n    "+message.content)
        print("[+] Sending command signal...")
        try:
            # We want it to respond if it replies with a command that does not
            # exist or is not available
            if context.message.command not in self.modules:
                raise exceptions.InvalidCommand
            dispatcher.send(signal=context.message.command,
                            ctx=context,
                            args=context.message.arguments)
        except exceptions.InvalidCommand:
            # Command doesn't exist
            print("[-] Command '{}' doesn't exist."\
                  .format(context.message.command))
            context.send("Sorry, invalid command.")
        except exceptions.InvalidArguments:
            # Invalid command arguments passed
            print("[-] Command '{}' was passed with invalid arguments."\
                  .format(context.message.command))
            context.send("Sorry, invalid arguments.")
        except exceptions.Restart:
            # Reload commands
            context.send("Restarting...")
            print("[=] Restarting...")
            print("=====================================")
            raise exceptions.Restart
        except Exception as e:
            # Unexpected error
            print("[-] Unexpected Error occured. Error logs here:\n\n"+e)
            context.send("Sorry, an unexpected error has occured.")
        print("=====================================")

    def initialize_listeners(self):
        """
        Start the following event listeners:
            on_message: called every time a message is sent/received
        """
        dispatcher.connect(self.on_message,
                           signal='on_message',
                           sender=dispatcher.Any)

    def listen(self):
        """
        This is the change dictionary that is returned
        {
            'old_val': None,
            'new_val': {
                'id': '0b60b000-7cc2-4886-a8ea-533eeccdf270',
                'info': '{}'
            }
        }
        """
        feed = r.table("Messages").changes().run(self.c)
        print("=====================================")
        for change in feed:
            initial_request = change['new_val']['info']
            message = initial_request['message']
            author = initial_request['sender']['id']
            timestamp = initial_request['timestamp']
            recipient = initial_request['recipient']['id']
            #print(json.dumps(initial_request,
            #                 indent=4,
            #                 sort_keys=True))
            message = contentTypes.Message(author=author,
                                           message=message,
                                           timestamp=timestamp,
                                           recipient=recipient)
            dispatcher.send(signal='on_message',
                            message=message)

def main():
    while True:
        try:
            Bot()
        except exceptions.Restart:
            pass
        except Exception as e:
            print("[-] Application crashed unexpectedly. Error logs here:\n\n")
            print(e)
            print("\n\n[+] Restarting...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("[-] Application exited due to manual keyboard input.")
