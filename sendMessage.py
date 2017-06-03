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
class Send:
    """Send messages"""

    def __init__(self, user_id : str):
        self.user_id = user_id
        self.token = ("EAASEeFpPvkABAJ9676sXYE1E8qeM7qOCCuuLkZB9lkYABmZCZAyZAk7"
                      "ZA6WHZBQlGNY0PlPGJOtcd81xv4ON2bhOeWMZBuUYRTP7ZCMq2K2jVDv"
                      "ZB0GhktwaQZCGldFSlN5udOYRY4pNEf6OdfwZCe6QvNL5uCwYMOcMTPg"
                      "Apkhv8Mx5gZDZD")

    def message_validate(self, message, payload=None):
        """
        Make a message readable by Facebook.

        This goes under 'message' for payloads
        {
            "content_type" : "text",
            "title" : #thereply,
            "payload" : "#whatisreturnedthroughcurl"
        }
        """
        to_return = {
                        "recipient" : {
                            "id" : self.user_id
                        },
                        "message" : {
                            "text" : message,
                        }
                    }
        if payload:
            to_return['message']['quick_replies'] = []
            for k, v in payload.items():
                quick_reply = {
                    "content_type" : "text",
                    "title" : k,
                    "payload" : v
                }
                to_return['message']['quick_replies'].append(quick_reply)
            else:
                print("[+] Added stuff to payload.")
        return to_return

    def send(self, message, payload=None):
        url = ("https://graph.facebook.com/v2.6/me/messages?"
               "access_token={}".format(self.token))
        if payload:
            to_reply = json.dumps(self.message_validate(message, payload))
        else:
            to_reply = json.dumps(self.message_validate(message))
        print("[+] Preparing to send message...")
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.POSTFIELDS, to_reply)
        c.setopt(c.HTTPHEADER, ['Content-Type: application/json'])
        c.perform()
        print("[+] Message sent to user '{}'.".format(self.user_id))
