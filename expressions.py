import re
import json

# enable regex patterns to pull from json files, allows easy future changes
flags = json.load(open('flags.json'))  # list
regs = json.load(open('registers.json'))  # dict
opCode = json.load(open('instructions.json'))  # dict
header = json.load(open('header.json'))  # string

patterns = {

    'output': r"^\./[\w]+/[\w]+\.mif$",
    # directory and file.mif

    'input': r'^(?:.*\n)*\s*\.' + flags[0] + r';(?P<' + flags[0] + r'>(?:.*\n)*)\s*\.' + flags[1] + r';(?:.*\n)*\s*\.'
             + flags[2] + r';(?P<' + flags[2] + r'>(?:.*\n)*)\s*\.' + flags[3] + r';(?:.*\n)*\s*\.' + flags[4] +
             r';(?P<' + flags[4] + r'>(?:.*\n)*)\s*\.' + flags[5] + r';(?:.*\n?)*$',
    # checks to see flags of form <.flag> in the order seen in flags.json, otherwise code is incomplete

    'comment': r"^(\s*;.*|)$",
    # comment lines start with a ";"

    'directive': r"^\.equ+\s+[a-zA-Z]+\s+0x[0-9a-fA-F]+;.*$",
    # <.equ> <name> <hex value>

    'constant': r"^\.word+\s+[a-zA-Z]+\s+0x[0-9a-fA-F]+;.*$",
    # <.word> <name> <hex value>

    'labeledLine': r"^@[\w]+\s+",
    # <@LabelName> <whatever>

    'arithLogi': r"^(?:@[0-9a-zA-Z]+\s+)?" + r"(?:{})".format('|'.join(map(re.escape, [*opCode]))) + r"+\s+" +
                 r"(?:{})".format('|'.join(map(re.escape, [*regs]))) + r"+,\s+" + r"(?:{})".format(
        '|'.join(map(re.escape, [*regs]))) + r"+;.*$",
    # <optional label> <instruction from json > <register from json, > <register from json; comment>

    'incDec': r"^(?:@[0-9a-zA-Z]+\s+)?" + r"(?:{})".format(
        '|'.join(map(re.escape, [*opCode]))) + r"+\s+" + r"(?:{})".format(
        '|'.join(map(re.escape, [*regs]))) + r"+,\s+0x[0-3];.*$",
    # <optional label> <instruction from json > <register from json, > <hex value; comment>

    'loadStore': r"^(?:@[0-9a-zA-Z]+\s+)?(LD|ST)\s+" + r"({})".format(
        '|'.join(map(re.escape, [*regs]))) + r",\s+M\[" + r"({})".format(
        '|'.join(map(re.escape, [*regs]))) + r",\s+0x[0-9a-fA-F]+\];.*$",
    # <optional label> <instruction from json > <register from json, > <M[register from json, hex offset]; comment>

    'jump': r"^(?:@[0-9a-zA-Z]+\s+)?JUMP\s+" + r"(Z|U),\s+" + r"@[\w]+;.*$",
    # <optional label> <JUMP> <Z or U> <@LabelName; comment>

    'pushPop': r"^(?:@[0-9a-zA-Z]+\s+)?(PUSH|POP)\s+" + r"({})".format('|'.join(map(re.escape, [*regs]))) + ";.*$"
    # <optional label> <push or pop> <register from json; comment>
}
