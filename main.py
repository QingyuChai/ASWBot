import itertools
import threading
import time
import sys

import callback
import rethinkdb as r

__version__ = "1.0.0"

done = False

def animate():
    for c in itertools.cycle(['|', '/', '-', "\\"]):
        if done:
            break
        sys.stdout.write('\rListening... ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rMessage:\n')

def start():
    t = threading.Thread(target=animate)
    t.start()

def main():
    c = r.connect()
    c.use("Facebook")

    feed = r.table("Messages").changes().run(c)
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

    start()

    for change in feed:
        initial_request = change['new_val']['info']
        message = initial_request['message']['text']
        user_id = initial_request['sender']['id']
        callback.Main(message,
                      user_id)
        done = True


if __name__ == "__main__":
    main()
