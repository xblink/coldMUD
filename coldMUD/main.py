#!/usr/bin/env python3

from interface.ircinterface import IRCInterface
from server import Server
import logging

if __name__ == '__main__':
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logger = logging.getLogger("coldMUD logger")
    
    iface = IRCInterface(logger=logger)
    iface.start()
    gameserver = Server(iface, logger=logger)
    gameserver.start()