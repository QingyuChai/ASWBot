import types
import urllib.request
import json
from datetime import datetime, timedelta
from random import randint as rand
from time import sleep

import checks
import exceptions
from pydispatch import dispatcher

__doc__ = """
This is a short documentation on commands.

How do I make a command acceptable by the program?

    def wrongcommand(ctx, args):
        print("This command won't work.")

    This is an example of a wrong command. Why so?
    The line above where it says "def wrongcommand(ctx, args):" is empty. That
    means our program doesn't recognize it as a command. How do we make it
    recognize it as a command? Look at the example below.

    @checks.command
    def rightcommand(ctx, args):
        This is an example of a working command. Compared
        print("This command will work.")

    What is different here? Above "def rightcommand(ctx, args):", there is
    something new: "@checks.command". This lets our program know that what we
    are executing is indeed a command and not a random function that just
    happens to be here.

How do I make my command send a message?

    First, let 'test' be the command you are making, and let 'whatyouwanttosend'
    be the message you are trying to send.

    Basically, we start with this:

        @checks.command
        def test(ctx, args):
            #Do something

    How do we make the bot reply?

        We use the function "ctx.send"

        @checks.command
        def test(ctx, args):
            message = 'whatyouwanttosend'
            ctx.send(message)   # <-- This line lets you send a message


        Basically what you do is write "ctx.send()", and inside the brackets you
        put down whatever you want the bot to write.

Full working example command below:
"""

# Note-to-self: Decorators are executed when file is started!

"""
Here are some more example commands
"""

@checks.command
def _eval(ctx,
          args):
    if not args:
        raise exceptions.InvalidArguments
    to_eval = " ".join(args)
    try:
        result = eval(to_eval)
    except:
        result = "Something went horrible wrong. Horribly, horribly wrong."
        print("[+] Something bad happened.")
    ctx.send(str(result))

@checks.command
def hi(ctx,
       args):
    message = "Hey there!"
    ctx.send(message)

@checks.command
def remind(ctx,
           args):
    argE = None
    if not args:
        argE = True
    elif len(args) < 2:
            argE = True
    else:
        try:
            int(args[0])
        except:
            argE = True
    if argE:
        raise exceptions.InvalidArguments

    print("[+] Sleep called for {} second(s).".format(args[0]))
    sleep(int(args[0]))
    print("[+] Sleep done.")
    ctx.send("Slept for {} second(s).".format(args[0]))
    ctx.send(" ".join(args[1:]))




@checks.command
def shutdown(ctx,
             args):
    ctx.send("Shutting down...")
    print("[=] Shutdown requested.")
    print("=====================================")
    exit()

@checks.command
def restart(ctx,
            args):
    raise exceptions.Restart


@checks.command
def help(ctx,
         args):
    if not args:
        payload = {
            'chucknorris' : 'chucknorris',
            'time' : 'time'
        }
        header = "Here are a list of commands:\n\n"
        commands = json.loads(open('modules.json','r').read())['modules']
        commands = ["| {} |".format(command) for command in commands]
        body = "\n".join(commands)
        ctx.send(header+body,
                 payload=payload)

@checks.command
def tic(ctx,
        args):
    ctx.send("Tac",
             payload={
                 'same':'lmao'
                 }
             )

@checks.command
def hello(ctx,
          args):
    ctx.send("how are you doing")

@checks.command
def chucknorris(ctx,
                args):
    """Chuck norris jokes"""
    url = "https://api.chucknorris.io/jokes/random"
    req = urllib.request.Request(url, headers={
        'User-Agent': 'Mozilla/5.0'
    })

    f = urllib.request.urlopen(req).read().decode('utf-8')
    joke = json.loads(f)['value']
    ctx.send(joke)

@checks.command
def time(ctx,
         args):
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
    ctx.send(msg)

@checks.command
def google(ctx,
           args):
    """Google something"""
    if not args:
        raise exceptions.InvalidArguments
        return
    s = "+".join(args)
    msg = "https://www.google.com/?q={s}#newwindow=1&q={s}".format(s=s)
    ctx.send(msg)

@checks.command
def example(ctx,
            args):
    """Example command"""
    # You want the 2 lines below IF you want to user to put in arguments,
    # such as "today", or "23"
    if not args:
        raise exceptions.InvalidArguments
        return
    msg = "Whatever you want as your reply"
    ctx.send(msg)

@checks.command
def reply(ctx,
          args):
    """Reply with your current message"""

    if not args:
        raise exceptions.InvalidArguments
        return

    msg = " ".join(args)
    ctx.send(msg)







"""

Ignore what is below here



def run_command(ctx):
    \"\"\"Choose what command to run\"\"\"
    message = ctx.message
    command_name = message.command
    args = message.arguments
    if args:
        arguments = " ".join(args)
    else:
        arguments = "None"
    print("[+] Command \"{}\" accepted... Checking "
          "for validity".format(command_name))
    print("    Arguments: "+arguments)

    try:
        com = eval(command_name)
        if isinstance(com, types.FunctionType):
            if 'is_command' in dir(com):
                eval("{}(ctx, args)".format(command_name))
                return
        raise NameError
    except NameError:
        raise exceptions.InvalidCommand
    except Exception as e:
        print("[-] Unexpected error. Check logs for details.")
        open("error.log", "w+").write("\n"+str(e)+"\n")

dispatcher.connect(run_command,
                   signal='command',
                   sender=dispatcher.Any)
"""
