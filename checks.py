import json

from pydispatch import dispatcher

__version__ = "1.0.0"
__doc__ = """
Checks for the Facebook bot
"""

def is_dev(func):
    def check(func):
        func.dev_only = True
        return func
    return check(func)

def command(func):
    def check(func):
        name = str(func.__name__).replace("_","")
        try:
            with open('modules.json', 'r') as f:
                modules = json.loads(f.read())
                modules['modules'].append(name)
        except Exception as e:
            print("[-] Error loading modules file. Shutting down.")
            exit()
        with open('modules.json', 'w') as f:
            f.write(json.dumps(modules,
                           indent=4,
                           sort_keys=True)
                )
        dispatcher.connect(func,
                           signal=name,
                           sender=dispatcher.Any)
        func.is_command = True
        return func
    return check(func)
