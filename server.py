#!/usr/bin/python3

from serverinterface import ServerInterface
import logging

class Server:
    def __init__(self, iface: ServerInterface, logger=logging.getLogger()):
        self.logger = logger
        self.interface = iface
        self.killcommands = [f"bye {self.interface.nick}"]

    def start(self):
        self.interface.start()
        self.logger.info("Server starting.")
        self.run()

    def run(self):
        while self.interface.connected:
            msg = self.interface.getmessage()
            if msg == "": continue

            if msg.find("PRIVMSG") != -1:
                self.handle_PRIVMSG(msg)

    def handle_PRIVMSG(self, msg: str):    
        name = msg.split('!', 1)[0][1:]
        payload = msg.split('PRIVMSG',1)[1]
        channel = payload.split(':',1)[0].strip()
        message = payload.split(':',1)[1]
        self.logger.info(f"[{channel}] {name}: {message}")
    
        if name in self.interface.admins:
            for command in self.killcommands:
                if message.find(command) == 0:
                    self.logger.info("Kill command recieved. Terminating.")
                    self.interface.sendmessage("oh...okay. :'(", channel)
                    self.interface._send("QUIT")
                    self.interface.terminate(1)

if __name__ == "__main__":
    print("Nope. Try 'python main.py' instead.")