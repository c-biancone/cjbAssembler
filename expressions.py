import re
import json

flags = json.load(open('flags.json'))  # list
regs = json.load(open('registers.json'))  # dict
opCode = json.load(open('instructions.json'))  # dict
header = json.load(open('header.json'))  # string

patterns = {
    'output': r"^\./[\w]+/[\w]+\.mif$",
    'input': r'^(?:.*\n)*\s*\.' + flags[0] + r';(?P<' + flags[0] + r'>(?:.*\n)*)\s*\.' + flags[1] + r';(?:.*\n)*\s*\.'
              + flags[2] + r';(?P<' + flags[2] + r'>(?:.*\n)*)\s*\.' + flags[3] + r';(?:.*\n)*\s*\.' + flags[4] +
              r';(?P<' + flags[4] + r'>(?:.*\n)*)\s*\.' + flags[5] + r';(?:.*\n?)*$',
    'comment': r"^(\s*;.*|)$",
    'directive': r"^\.equ+\s+[a-zA-Z]+\s+0x[0-9a-fA-F]+;.*$",
    'constant': r"^\.word+\s+[a-zA-Z]+\s+0x[0-9a-fA-F]+;.*$",
    'labeledLine': r"^@[\w]+\s+",
    'arithLogi': r"^(?:@[0-9a-zA-Z]+\s+)?" + r"(?:{})".format('|'.join(map(re.escape, [*opCode]))) + r"+\s+" +
                 r"(?:{})".format('|'.join(map(re.escape, [*regs]))) + r"+,\s+" + r"(?:{})".format(
        '|'.join(map(re.escape, [*regs]))) + r"+;.*$",
    'incDec': r"^(?:@[0-9a-zA-Z]+\s+)?" + r"(?:{})".format(
        '|'.join(map(re.escape, [*opCode]))) + r"+\s+" + r"(?:{})".format(
        '|'.join(map(re.escape, [*regs]))) + r"+,\s+0x[0-3];.*$",
    'loadStore': r"^(?:@[0-9a-zA-Z]+\s+)?(LD|ST)\s+" + r"({})".format(
        '|'.join(map(re.escape, [*regs]))) + r",\s+M\[" + r"({})".format(
        '|'.join(map(re.escape, [*regs]))) + r",\s+0x[0-9a-fA-F]+\];.*$",
    'jump': r"^(?:@[0-9a-zA-Z]+\s+)?JUMP\s+" + r"(Z|U),\s+" + r"@[\w]+;.*$",
    'pushPop': r"^(?:@[0-9a-zA-Z]+\s+)?(PUSH|POP)\s+" + r"({})".format('|'.join(map(re.escape, [*regs]))) + ";.*$"
}
