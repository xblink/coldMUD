from abc import ABC, abstractmethod

class ServerInterface(ABC):
    def __init__(self):
        super.__init__()

    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def sendmessage(self, message):
        pass

    @abstractmethod
    def getmessage(self, message):
        pass

    @abstractmethod
    def terminate(self, message):
        pass