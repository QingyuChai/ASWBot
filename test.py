__doc__ = """
Testing out features
"""

import checks

@checks.command
def pleasework():
    pass


print(pleasework.is_command)
if 'is_command' in dir(pleasework):
    print("YEE")
