from interface.serverinterface import ServerInterface
from expressionparser import parser as ep
import logging
from queue import SimpleQueue

class Server:
    """coldMUD game server"""
    players = []
    commandqueue = SimpleQueue()

    def __init__(self, iface: ServerInterface, logger=logging.getLogger()):
        self.interface = iface
        self.logger = logger
        self.killcommands = [f"bye {self.interface.nick}"]

    def start(self):
        self.logger.info("Server starting.")
        self.run()

    def run(self):
        while self.interface.is_connected:
            msg = self.interface.getmessage()
            if msg == "": continue

            if msg.find("PRIVMSG") != -1:
                self.handle_PRIVMSG(msg)

            self.do_commands()

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

        if name in self.players:
            command = ep.parse(message)
            self.commandqueue.put((name, command))

    def do_commands(self):
        if not self.commandqueue.empty:
            player, command = self.commandqueue.get()
            self.logger.info(f"{player}: {command}")
            # execute order 66


if __name__ == "__main__":
    print("Nope. Try 'python main.py' instead.")