from basecommand import Command
from basecommand import CommandTypes as cType

def parse(message) -> Command:
    return Command(cType.IDLE)

if __name__ == "__main__":
    print("Try 'python main.py")