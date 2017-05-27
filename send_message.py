import json
import sys
import subprocess
import pycurl

__version__ = "1.0.2"
__doc__ = """
Send messages on Facebook
"""

LISTOFQUOTES = [
    'quote 1',
    'quote 2',
    'quote 3'
]

#str_replace("<break/>")
class SendMessage:
    """Send messages"""

    def __init__(self, user_id : str):
        self.user_id = user_id
        #self.token = open('/var/www/fwiedwice.me/fbot/fbot/token.txt', 'r').read()
        self.token = "EAASEeFpPvkABAJ9676sXYE1E8qeM7qOCCuuLkZB9lkYABmZCZAyZAk7ZA6WHZBQlGNY0PlPGJOtcd81xv4ON2bhOeWMZBuUYRTP7ZCMq2K2jVDvZB0GhktwaQZCGldFSlN5udOYRY4pNEf6OdfwZCe6QvNL5uCwYMOcMTPgApkhv8Mx5gZDZD"

    def message_validate(self, message):
        to_return = {
                        "recipient" : {
                            "id" : self.user_id
                        },
                        "message" : {
                            "text" : message,
                            "quick_replies":[
                                {
                                    "content_type":"text",
                                    "title":"chucknorris",
                                    "payload":"nothing"
                                },
                                {
                                    "content_type":"text",
                                    "title":"time",
                                    "payload":"nothing"
                                },
                                {
                                    "content_type":"text",
                                    "title":"tic",
                                    "payload":"nothing"
                                }
                            ]
                        }
                    }
        return to_return

    def send(self, message):
        url = ("https://graph.facebook.com/v2.6/me/messages?"
               "access_token={})".format(self.token))
        to_reply = json.dumps(self.message_validate(message))
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.POSTFIELDS, to_reply)
        c.setopt(c.HTTPHEADER, ['Content-Type: application/json'])
        c.perform()
