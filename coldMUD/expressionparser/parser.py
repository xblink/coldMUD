from .basecommand import Command
from .basecommand import CommandTypes as cType
import json

dictFiles = ["verbs", "delimiters"]
vocab = {}

def build_dictionaries():
    for file in dictFiles:
        vocab[file] = fetch_dict_json(file)

def parse(message) -> Command:
    parsedCommands = []
    commands = tokenize(message)

    for c in commands:
        newCommand = Command(cType.NONE)
        if c[0] in vocab["verbs"]["commands"]["help"]:
            newCommand = Command(cType.HELP)
        parsedCommands.append(newCommand)

    return parsedCommands

def tokenize(msg: str) -> list:
    tokens = msg.split(" ")
    tokens = handle_delimiters(tokens)
    commands = split_into_commands(tokens)
    return commands

def handle_delimiters(rawTokens: list) -> list:
    tokens = []
    for token in rawTokens:
        if len(token) > 1 and token[-1] in vocab["delimiters"]:
            tokens.append(token[:-1])
            tokens.append(token[-1:])
        else:
            tokens.append(token)

    return tokens

def split_into_commands(tokens: list) -> list:
    start = 0
    commands = []
    for i in range(0, len(tokens)):
        command = []
        if tokens[i] in vocab["delimiters"]:
            command = tokens[start:i]
            start = i + 1
        elif i == len(tokens) - 1:
            command = tokens[start:]
            
        if command != []:
            commands.append(command)
    
    print(commands)
    return commands

def fetch_dict_json(filename:str):
    data = None
    path = "coldmud/expressionparser/dict/"+filename+".json"
    with open(path, "r") as read_file:
        data = json.load(read_file)
    return data


if __name__ == "__main__":
    print("Try 'python main.py")