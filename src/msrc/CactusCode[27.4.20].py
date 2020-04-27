import os
import sys
import re
import time
import random
import tkinter as tk
import CactusCompiler

sourceCode = ""
chrLoc = 0
variables = []
roots = []

class variable:
    def __init__(var, name = None, value = None):
        var.name = name
        var.value = value

class root:
    def __init__(root, name = None, requireVals = None, value = None):
        root.name = name
        root.requireVals = requireVals
        root.value = value

"""
fileOfSource = input("CactusCode >> ")
file = open(fileOfSource, "r")
sourceCode = file.read()
file.close()
"""

def handleFinish():
    print("CactusCode >> Finished received. Printing final information\n")
    print("CactusCode >> MundaneInformation = [ Author:ShaunCameron, Name:CactusCode, Version:0.1a, Release:False ]")
    #Add 0.1 to Version each week, limit of 0.15 (per alpha, beta, release OR [a, b, r])
    print("CactusCode >> Variables = [ {} ]".format(", ".join(["{}:{}".format(x.name, x.value) for x in variables])))
    quit()

def compress():
    global chrLoc
    global sourceCode
    global variables
    global roots

    while chrLoc < len(sourceCode) and sourceCode[chrLoc] in [" ", "\t", "\n"]:
        chrLoc += 1

def handleComment():
    global chrLoc
    global sourceCode

    while chrLoc < len(sourceCode) and sourceCode[chrLoc] != "\n":
        chrLoc += 1
    chrLoc += 1

def handleSet():
    global sourceCode
    global chrLoc
    global variables
    global regexChecks

    var = variable()

    var.name = re.findall(r"^set+?\s*([a-zA-Z0-9]+)+?\s*to", sourceCode[chrLoc:])[0]

    if var.name.startswith("$") or var.name.startswith("_"):
        print("CactusCode >> %i >> found illegal variable prefix. You can't start a variable with either '$' or '_'"%chrLoc)
        quit()

    chrLoc += 3
    compress()
    chrLoc+= len(var.name)
    compress()
    chrLoc += 2
    compress()

    var.value = ""

    if re.match(r"true", sourceCode[chrLoc:]):

        var.value = True
        chrLoc += 4

    elif re.match(r"false", sourceCode[chrLoc:]):

        var.value = False
        chrLoc += 5

    elif sourceCode[chrLoc] == "'":
        chrLoc += 1
        while sourceCode[chrLoc] != "'":
            var.value += sourceCode[chrLoc]
            chrLoc += 1

    elif sourceCode[chrLoc] == '"':
        chrLoc += 1
        while sourceCode[chrLoc] != '"':
            var.value += sourceCode[chrLoc]
            chrLoc += 1

        var.value = str(var.value)

    elif re.match(r"^[0-9]", sourceCode[chrLoc]):

        varInteger = re.match(r"^([0-9]+)", sourceCode[chrLoc:])[0]

        var.value = float(varInteger)
        chrLoc += len(str(varInteger))

    elif re.match(r"^\$([a-zA-Z0-9]+)", sourceCode[chrLoc:]):
        if re.match(r"^\$([a-zA-Z0-9]+)", sourceCode[chrLoc:])in [("$"+x.name) for x in variables]:
            print("found match!")

    else:
        print("CactusCode >> Tried to 'root' a variable assignment '{}' but illegal identifier '{}' was found!".format(var.name, sourceCode[chrLoc]))
        handleFinish()

    chrLoc += 1
    compress()

    variables.append(var)
    #print(var.name,"=",var.value,type(var.value))

def cleanValue(value):
    for x in variables:
        value = value.replace(("$"+x.name), str(x.value))

    return value

def handleMessage():
    global chrLoc
    global sourceCode

    chrLoc += 3
    compress()
    chrLoc += 2

    messageValue = ""

    while sourceCode[chrLoc] != '"':
        messageValue += sourceCode[chrLoc]
        chrLoc += 1

    chrLoc += 2
    compress()

    print(cleanValue(messageValue))

def handleRoot():
    CactusCompiler.pt.textarea.insert("Yeet")
    global chrLoc
    global sourceCode
    global roots

    subr = root()

    print(sourceCode[chrLoc:])
    rootValues = re.findall(r"^@root\s*([a-zA-Z0-9]+)\[(.*)]\s*{([\S\s]*)} break root", sourceCode[chrLoc:])[0]

    subr.name = rootValues[0]
    subr.requireVals = rootValues[1]

    chrLoc += 5
    compress()
    chrLoc += len(rootValues[0]) + 2 + len(rootValues[1])
    chrLoc += 2
    compress()

    subr.value = ""
    while not re.match(r"^} break root", sourceCode[chrLoc:]):
        subr.value += sourceCode[chrLoc]
        chrLoc += 1

    chrLoc += 12
    compress()

    roots.append(subr)

def handleCallRoot():
    def cleanRootValue(messageValue):
        pass

    def handleRootComment():
        global tempChrLoc
        global rootCode


        while tempChrLoc < len(rootCode) and rootCode[tempChrLoc] != "\n":
            tempChrLoc += 1
        tempChrLoc += 1

    global chrLoc
    global sourceCode
    global roots

    subr = re.findall(r"^@([a-zA-Z0-9]+)\[(.*)]", sourceCode[chrLoc:])[0]

    chrLoc += re.match(r"^@([a-zA-Z0-9]+)\[(.*)]", sourceCode[chrLoc:]).span()[-1]

    f = False
    rootCode = ""
    rootCodeReq = ""
    for x in roots:
        if subr[0] == x.name:
            f = True
            rootCode = x.value
            rootCodeReq = x.requireVals

    if f == False:
        print("Cactus Code >> Couldn't find a (root|subroutine) called '%s'!"%subr[0])
        handleFinish()

    tmpVars = [cleanValue(x) for x in subr[1].split(",")]
    for x in tmpVars:
        while x.startswith(" "):
            x = x[1:]

    if len(tmpVars) != len(rootCodeReq.split(",")):
        print("Cactus Code >> Either too many or not enough arguments")
        handleFinish()

    tempChrLoc = 0
    while tempChrLoc < len(rootCode):
        if rootCode[tempChrLoc:].startswith("//"):
            handleRootComment()
            continue

def compile(src):
    global chrLoc
    global variables
    global roots
    global sourceCode

    sourceCode = src

    while chrLoc < len(sourceCode):
        #print(sourceCode[chrLoc:], chrLoc)
        # Comments
        if sourceCode[chrLoc:].startswith("//"):
            handleComment()
            continue
        # Variables setting
        if re.match(r"^set+?\s*([a-zA-Z0-9]+)+?\s*to", sourceCode[chrLoc:]):
            handleSet()
            continue
        # Message handling
        if re.match(r"^say+?\s*\{", sourceCode[chrLoc:]):
            handleMessage()
            continue

        # Root (Subroutine) making handling
        if re.match(r"^@root\s*([a-zA-Z0-9]+)\[(.*)]\s*{([\S\s]*)} break root", sourceCode[chrLoc:]):
            handleRoot()
            continue

        # Root (subroutine) calling handling

        if re.match(r"^@([a-zA-Z0-9]+)\[(.*)]", sourceCode[chrLoc:]):
            handleCallRoot()
            continue


        chrLoc += 1

        handleFinish()

"""
with open("main.cactus", "r") as file:
    compile(file.read())
print("CactusCode >> Roots = [ {} ]".format(", ".join(["{}:{}:{}".format(x.name, x.requireVals, x.value) for x in roots])))
Need to add loops using regex
Need to add locations using regex
Need to add say keyword
Need to replace variables when setting them again
Need to have procedural calculations in setting
Need to support placeholedrs in variables, if type is correct
Need to add if and else using regex

@extend Janitor @extend Jess @extend Sherlock
Add Janitor compiler extension to clean up un needed bits of code on file run
Add Jess compiler extension to show errors (If instructed, runs before Janitor)
Add Sherlock interpreter extension for regex understanding, as well as other cybersecurity things
"""
