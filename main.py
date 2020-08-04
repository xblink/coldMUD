#!/usr/bin/python3

from ircinterface import IRCInterface
from server import Server
import logging

if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logger = logging.getLogger("coldMUD logger")
    
    interface = IRCInterface(logger=logger)
    gameserver = Server(interface, logger=logger)
    gameserver.start()