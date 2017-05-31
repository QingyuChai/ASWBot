import json

from pydispatch import dispatcher

__version__ = "1.0.0"
__doc__ = """
Checks for the Facebook bot
"""

def command(func):
    def check(func):
        try:
            with open('modules.json', 'r') as f:
                modules = json.loads(f.read())
                modules['modules'].append(func.__name__)
        except Exception as e:
            print("[-] Error loading modules file. Shutting down.")
            exit()
        with open('modules.json', 'w') as f:
            f.write(json.dumps(modules,
                           indent=4,
                           sort_keys=True)
                )
        dispatcher.connect(func,
                           signal=func.__name__,
                           sender=dispatcher.Any)
        func.is_command = True
        return func
    return check(func)
