#!/usr/bin/env python
"""
cjbASM program to convert custom Assembly language files for cjbRISC processor into Machine Code Memory Initialization
Files (.mif) used to load the programs onto the CPU at compile time.
First verifies correct usage, then correct input file syntax, and finally assembles the output file with necessary
computations.

Example Test Cases:
    ./cjbASM.py ./test/HelloWorld.txt ./out/HelloWorld.mif  # Will produce working code to print Hello, World! in ASCII
    ./cjbASM.py ./test/neuralNetMult.txt ./out/neuralNetMult.mif  # Simulates multiplication algorithm for neural net
    ./cjbASM.py ./test/broken.txt ./out/broken.mif          # Will not compile, see that the assembler shows line error

Python Version: 3.10.2
"""
__author__ = "Chris Biancone"
__version__ = "1.0"

import sys, json, re
from nltk.tokenize import word_tokenize as tokenize  # tokenizes words and punctuation - ideal for assembler
from expressions import patterns  # local RegEx patterns dictionary for readability

# this file needs access to json files as well as expressions.py for assembly
flags = json.load(open('flags.json'))  # list
regs = json.load(open('registers.json'))  # dict
opCode = json.load(open('instructions.json'))  # dict
header = json.load(open('header.json'))  # string
# set up global lists and dictionaries for storing data to be accessed in multiple methods
directives, constants, labels, code = dict(), dict(), dict(), dict()
directiveFile, constantFile, opcode, codeFile = list(), list(), list(), list()


def verify_flags(group, flag_list, string):
    """
        Verifies correct compiler directive and constants syntax
        Currently are expected but used as placeholders

        :param group: RegEx group of code between flags
        :param flag_list: list to add found flags to
        :param string: name for pattern key and error msg
        :return: N/A
        """
    for line in group.splitlines():
        # TODO: implement independent usage for assembler directives and constants (future)
        line = line.strip()  # remove leading and trailing whitespace
        comment = re.search(patterns['comment'], line)  # match regex pattern for comment line <; word chars>
        if not comment:  # if not comment or blank line
            flag = re.search(patterns[string], line)  # match regex pattern for argument type
            if not flag: raise SyntaxError("Incorrect" + string + "syntax at line: " + line)
            else:
                lineList = tokenize(line)
                flag_list[lineList[1]] = lineList[2]  # grab for future processing


def verify_code(group):
    """
    Verifies correct code syntax, then tokenizes code for assembling

    :param group: RegEx group of assembly code lines
    :return: N/A
    """
    iLine = 0
    for line in group.splitlines():
        line = line.strip()  # leading and trailing whitespace
        comment = re.search(patterns['comment'], line)
        if not comment:
            code[iLine] = dict()  # create multilevel dictionary sorted by code line for different code attributes
            labeledCode = re.search(patterns['labeledLine'], line)  # look for labels
            if labeledCode:  # label must occur before first jump instruction
                lineList = tokenize(line)
                code[iLine].update({'labeled': True, 'label': lineList[0] + lineList[1]})
                labels[lineList[0] + lineList[1]] = iLine  # store to grab line of code later
                del lineList[0:2]  # remove label from line before reprocessing
        # try and match line to correct syntax for a type of assembly instruction
        # looks for instruction, source/destination register, and source register or offset
            arithLogi = re.search(patterns["arithLogi"], line)
            incDec = re.search(patterns['incDec'], line)
            loadStore = re.search(patterns['loadStore'], line)
            jump = re.search(patterns['jump'], line)
            pushPop = re.search(patterns['pushPop'], line)
            if arithLogi or incDec or jump or pushPop:
                if not labeledCode:
                    lineList = tokenize(line)
                code[iLine].update({'inst': lineList[0], 'Rsd': lineList[1]})
                codeFile.append(line)  # raw code line for comments in output file
                if jump:  # different for conditional (Z) / unconditional (U)
                    if lineList[1] == 'Z': code[iLine].update({'Rs': '01', 'type': 'jump', 'label': lineList[3] + lineList[4]})
                    else: code[iLine].update({'Rs': '00', 'type': 'jump', 'label': lineList[3] + lineList[4]})
                elif pushPop:
                    code[iLine].update({'Rs': '00', 'type': 'pushPop'})  # stack operation, Rs NULL
                elif incDec:  # hex increment value to binary
                    code[iLine].update({'Rs': format(int(lineList[3], 16), '08b')[-2:], 'type': 'incDec'})
                else:
                    code[iLine].update({'Rs': regs[lineList[3]], 'type': 'arithLogi'})
            elif loadStore:  # requires inclusion of memory offset, converted from hex
                if not labeledCode: lineList = tokenize(line)
                code[iLine].update({'inst': lineList[0], 'Rsd': lineList[1], 'Rs': regs[lineList[5]],
                                    'memOffset': format(int(lineList[7], 16), '08b')[-8:], 'type': 'loadStore'})
                codeFile.append(line)
            else:
                raise SyntaxError("At raw code line "+str(iLine)+": "+line)
            iLine += 1  # increment only if not comment


def assemble(output):
    """
    Performs assembly of machine code using tokenized code lines. Pulls from data files.
    Computes necessary offsets and performs conditional assembling for certain instructions.
    Writes memory initialization file.

    :param output: output filename
    :return: N/A
    """
    # TODO: develop syntax to copy over header from ASM to MIF
    outFile = open(output, 'w')
    outFile.write(header)
    labelPCs = dict()
    pc = 0
    for line in code:  # this has been turned into a 3-pass assembler to allow for lookahead on the JUMP instruction
        if 'labeled' in code[line]:
            labelPCs[code[line]['label']] = pc
        pc += 1
        if code[line]['type'] == 'jump' or code[line]['type'] == 'loadStore':
            pc += 1
    pc = 0
    for line in code:  # this loop does the real assembly, replacing ASM w/ MC
        # print <hex program line> : <4-bit opcode><2-bit source/destination reg><2-bit source reg>
        #       optional 8-bit offset for JUMP, LOAD, STORE
        outFile.write(
            format(pc, '04x') + " : " + opCode[code[line]['inst']] + regs[code[line]['Rsd']] + code[line]['Rs'] +
            ";  % " + codeFile[line] + " %\n")
        if code[line]['type'] == 'jump':  # requires memory offset calculation based on cjbRISC architecture
            pc += 1
            try:
                outFile.write(
                    format(pc, '04x') + " : " + format((1024 + labelPCs[code[line]['label']]) - pc, '08b')[-8:] + ";\n")
            except: raise SyntaxError("JUMP label mismatch in code line " + str(line) + ": " + codeFile[line])
        elif code[line]['type'] == 'loadStore':
            pc += 1
            outFile.write(format(pc, '04x') + " : " + code[line]['memOffset'] + ";\n")
        else:  # no second line necessary
            pass
        pc += 1
    outFile.write("\n[" + format(pc, '04x') + "..03FF] : 00000000; % Fill the remaining locations with 0 %\nEND;")


def main():
    """
    Checks correct usage syntax and runs verification and assembly routines.

    :return: if incorrect usage
    """
    if len(sys.argv) != 3 or not re.search(patterns['output'], sys.argv[2]):  # invalid input name intrinsically handled
        print('cjbASM.py usage: <./cjbASM.py ./dir/inASMname.txt ./dir/outMCname.mif')
        sys.exit(-1)  # throw a nice error code
    inFile = open(sys.argv[1], 'r')
    correctFileSyntax = re.search(patterns['input'], inFile.read())
    if not correctFileSyntax: raise SyntaxError("Incorrect flag structure, cannot parse ASM file")
    verify_flags(correctFileSyntax.group(flags[0]), directives, "directive")
    verify_flags(correctFileSyntax.group(flags[2]), constants, "constant")
    verify_code(correctFileSyntax.group(flags[4]))
    assemble(sys.argv[2])
    print("Assembly Successful!!")


if __name__ == "__main__":
    main()
