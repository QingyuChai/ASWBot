import json
import asyncio
import contentTypes

from pydispatch import dispatcher

__version__ = "1.0.0"
__doc__ = """
Checks for the Facebook bot
"""

import inspect


def getSource(meth):
    if inspect.ismethod(meth):
        for cls in inspect.getmro(meth.__self__.__class__):
            if cls.__dict__.get(meth.__name__) is meth:
                return cls
        meth = meth.__func__  # fallback to __qualname__ parsing
    if inspect.isfunction(meth):
        cls = getattr(
            inspect.getmodule(meth),
            meth.__qualname__.split(
                '.<locals>',
                1)[0].rsplit(
                '.',
                1)[0])
        if isinstance(cls, type):
            return cls
    return None

commands = {}


def command(name=None):
    def check(func):
        setattr(func, 'is_command', True)
        if name:
            setattr(func, '__name__', name)
            setattr(func, 'name', name)
        func.is_command = True
        return func
    return check


def getCommands():
    return commands
