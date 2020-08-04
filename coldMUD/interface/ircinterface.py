#!/usr/bin/python3

from interface.serverinterface import ServerInterface
from interface.interfacestates import State

from getpass import getpass
import logging
import socket
import threading


class IRCInterface(ServerInterface):
    """IRC Interface for coldMUD"""

    def __init__(self, server="irc.frogbox.es", 
                       channels=["#botter"], 
                       logger=logging.getLogger()):

        self.logger = logger
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = 6667
        self.channels = channels
        self.nick = "blinker"
        self.admins = ["xblink"]

        self.connected = State.NONE
        self.registered = State.NONE
        self.identified = State.NONE

        self._ibufferlock = threading.Lock()
        self.inputbuffer = []

    def start(self):
        self.connect()
        self.authenticate()

        for chan in self.channels:
            self.joinchannel(chan)

        self.listen()

    def _send(self, message):
        self.sock.send(bytes(message + "\r\n", "UTF-8"))

    def _recv(self) -> str:
        return self.sock.recv(2048).decode("UTF-8")

    def connect(self):
        self.sock.connect((self.server, self.port))
        self._send("NICK " + self.nick)
        self._send("USER {0} {0} {0} :{1}'s Bot".format(
            self.nick, self.admins[0]))

    def authenticate(self):
        while (self.registered != State.ACTIVE and 
               self.identified not in [State.ACTIVE, State.DISABLED]):
            msg = self._recv()
            for line in msg.splitlines():
                self.logger.debug(line)
            self.handle_message(msg)
            
            if self.identified == State.REQUESTED:
                self.prompt_password()

    def handle_message(self, msg: str):
            if msg.find("PING :") != -1:
                payload = msg.split('PING', 1)[1].split(':', 1)[1]
                self._send("PONG :" + payload)

            if msg.find("NOTICE * :*** Found your hostname") != -1:
                self.connected = State.ACTIVE
                self.logger.info(f"Connected to {self.server}:" + 
                                  f"{self.port} as {self.nick}")

            if msg.find(f":{self.nick} MODE {self.nick} :+iwx") != -1:
                self.registered = State.ACTIVE
                self.logger.info(f"Nick {self.nick} registered.")

            if msg.find(f":NickServ MODE {self.nick} :+r") != -1:
                self.identified = State.ACTIVE
                self.logger.info(f"Nick {self.nick} identified.")

            if msg.find(f"NOTICE {self.nick} :This nickname is regi") != -1:
                self.identified = State.REQUESTED

            if msg.find(f"NOTICE {self.nick} :Password incorrect.") != -1:
                self.identified = State.REQUESTED
                print ("Password incorrect.")

    def prompt_password(self):
        psw = getpass()
        if psw == "":
            self.identified = State.DISABLED
        else:
            self.sendmessage("IDENTIFY {0}".format(psw), "NickServ")
            self.identified = State.PENDING

    def joinchannel(self, chan: str):
        self.logger.info("Joining channel {0}.".format(chan))
        self._send("JOIN " + chan)
        msg = ""

        while msg.find("End of /NAMES list.") == -1:
            msg = self._recv()
            for line in msg.splitlines():
                self.logger.debug(line)

        self.logger.info("Joined channel {0} sucessfully.".format(chan))

    def sendmessage(self, message: str, target: str):
        self._send(f"PRIVMSG {target} :{message}")

    def listen(self):
        self.logger.info("Creating listener thread.")
        self.listenerthread = threading.Thread(target=self.listen_thread)
        self.listenerthread.start()
        self.logger.info("Listener thread started.")

    def listen_thread(self):
        while self.connected:
            msg = self._recv()
            if msg == "": continue

            if msg.find("PING") == 0:
                self.logger.info(msg)
                self._send("PONG :Anybody home?")

            if msg[1:].split(':',1)[0].find(" PRIVMSG ") != -1:
                self.logger.debug(msg.rstrip("\r\n"))
                with self._ibufferlock:
                    self.inputbuffer.append(msg)

        self.logger.info("Listener thread terminating.")

    def getmessage(self) -> str:
        msg = ""
        with self._ibufferlock:
            if len(self.inputbuffer) > 0:
                msg = self.inputbuffer[0]
                self.inputbuffer.pop(0)
        return msg

    def terminate(self, message):
        self.logger.info("Terminating service.")
        self.connected = False
        self.listenerthread.join()
        self.sock.shutdown(message)
        self.sock.close()
        self.logger.info("Socket closed.")


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG,
                            datefmt="%H:%M:%S")
    iface = IRCInterface()
    iface.start()