from . import checks

__doc__ = """
Example module
"""

@checks.command
def hi(args):
    """nothing much"""
    self.send('Hi')
