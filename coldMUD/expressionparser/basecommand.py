class CommandTypes:
    """Command Object Types Enumeration"""
    NONE = "none"
    IDLE = "idle"
    HELP = "help"

class Command:
    """Command Object"""
    commandType = None
    context = None

    def __init__(self, commandType):
        self.commandType = commandType