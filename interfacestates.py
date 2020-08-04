class InterfaceStateEnum():
    @property
    def NONE(self): return -1
    @property
    def REQUESTED(self): return 0
    @property
    def ACTIVE(self): return 1
    @property
    def DISABLED(self): return 2
    @property
    def PENDING(self): return 3

State = InterfaceStateEnum()