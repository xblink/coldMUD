class CommandTypes:
    """Command Object Types Enumeration"""
    @property
    def NONE(self): return None
    @property
    def IDLE(self): return "idle"
    @property
    def MOVE(self): return "move"
    @property
    def ATTACK(self): return "attack"
    @property
    def DODGE(self): return "dodge"
    @property
    def BLOCK(self): return "block"

class Command:
    """Command Object"""
    commandType = CommandTypes.NONE
    context = None

    def __init__(self, commandType):
        self.commandType = commandType

    def __str__(self):
        return self.commandType
        