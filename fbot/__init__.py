import json
import asyncio
import websockets
import platform
from flask import Flask, request
import rethinkdb as r

c = r.connect()
c.use("Facebook")

app = Flask(__name__)

"https://developers.facebook.com/docs/messenger-platform/webhook-reference#subscribe"

VERIFY_TOKEN = "TheTokenIsReal"

@app.route("/")
def hello():
    return "asd"
           #(open("fbot/index.html", "r").read()\
            #.format(pyver=platform.python_version()))

@app.route("/test")
def secret():
    return "Testing python-hosted webserver."

@app.route("/test/test")
def secret2():
    return "Testing more complicated file path"

@app.route("/callback", methods=['GET', 'POST'])
def _callback():
    """Facebook sends a request to this part of the code"""

    print(request.method)
    if request.method == 'GET':
        hub_verify = request.args.get('hub.verify_token', '')
        if hub_verify == VERIFY_TOKEN:
            print(request.args.get('hub.challenge'))
            return request.args.get('hub.challenge')
        else:
            return 'Nothing?'
    elif request.method == 'POST':
        try:
            initial_request = request.get_json()['entry'][0]['messaging'][0]
            # Check if it is a message
            message = initial_request['message']['text']
            user_id = initial_request['sender']['id']
            print("\n=-=-=-=-=")
            print("Request went through!")
            print("=-=-=-=-=\n")
            async def hello():
                async with websockets.connect('ws://localhost:1111') as websocket:

                    reply = await websocket.send(str(initial_request))

            asyncio.get_event_loop().run_until_complete(hello())

            return "POST, but careful"
        except Exception as e:
            print("\n=-=-=-=-=")
            print("Request did not go through.")
            print(e)
            print("=-=-=-=-=\n")
            return "Error"
    else:
        print("Else statement got triggered")
        return "Anything else"

if __name__ == "__main__":
    app.run()
