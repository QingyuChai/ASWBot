class InvalidArguments(Exception):
    def __init__(self):
        self.message = "[-] Invalid Arguments passed."

    def __str__(self):
        return self.message

class InvalidCommand(Exception):
    def __init__(self):
        self.message = "[-] Invalid Command called."

    def __str__(self):
        return self.message

class TooManyMessages(Exception):
    pass
