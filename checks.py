__version__ = "1.0.0"
__doc__ = """
Checks for the Facebook bot
"""

def command(func):
    def check(func):
        func.is_command = True
        return func
    return check(func)
