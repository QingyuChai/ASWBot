# README - ASWBot

# Very important information

- How do I set up a module file?

You import the files *checks* and *exceptions*.

```python

# mymodule.py

import checks

```

That's all you need to set up a module for ASWBot. Easy.

- How do I make a command?

First, you have to make a normal python function, that accepts the arguments
*ctx* and *args*. On top of the function, you need to add a decorator,
*@checks.command*, or it won't be registered as a command.

```python

@checks.command
def mycommand(ctx,
              args):
    pass
```

This would be a command that does... nothing.
Now, how do I make this command reply to a user? That's what we have *ctx* for.

You have to use the *send* function, which is an attribute of ctx.

```python

@checks.command
def mycommand(ctx,
              args):
    ctx.send("mymessagetotheworld")
```

There we go! Not that hard, right?

A full example module would look like this

```python

#mymodule.py   <-- the name of the file

import checks

@checks.command
def commandone(ctx,
               args):
    ctx.send("This is my first command!")

@checks.command
def commandtwo(ctx,
               args):
    ctx.send("This is my second command!")
```

# Advanced area

- How do I send a quick reply?

To send a quick reply, you need a to make a one-dimensional python dictionary.

```python
my_quick_reply = {
    "theReplyItSuggests" : "anything",
    "anotherReplyItSuggests" : "anything"
}
```

The next step is sending it. We still use *ctx.send* for this.

```python

ctx.send("myMessage", payload=my_quick_reply)

```

- How do I get command arguments?

- How do I manage exceptions?
