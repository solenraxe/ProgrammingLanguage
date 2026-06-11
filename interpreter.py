import os
import memory

global currentLine, currentScript
currentLine = 0
currentScript = []
embedCount = 0

def getFollowingLines():
    global currentLine, currentScript, embedCount
    lines = []
    i = 0
    init = (embedCount - 1) * 2
    while currentLine + i < len(currentScript) and currentScript[currentLine + i][init:].startswith("- "):
        lines.append(currentScript[currentLine + i][init+2:])
        i += 1
        
    return lines

def getValue(valueType, value):
    newVal = 0
    if valueType == None: return int(value)
    if valueType == "nbr" or valueType == "int":
        newVal = int(value)
    elif valueType == "dec" or valueType == "float":
        newVal = float(value)
    elif valueType == "txt" or valueType == "str":
        newVal = str(value)
    elif valueType == "truth" or valueType == "bool":
        newVal = value.lower() == "true"
    elif valueType == "var":
        newVal = memory.getVar(value) or 0
    elif valueType == "list":
        string = value
        newVal = string.split(",")
        if string.find(".") != -1:
            numIndex = string.find(".") + 1
            indexIsVar = memory.getVar(string[numIndex:]) != None
            index = memory.getVar(string[numIndex:]) if indexIsVar else int(string[numIndex:])
            list = memory.getVar(string[:numIndex-1])
            if len(list) > index:
                newVal = list[index]
            else:
                newVal = "invalid"

    return newVal

def ifInter(args):
    comparators = args["comp"]
    if not comparators:
        return args["obj1"]
    
    valid = False
    for comp in comparators:
        if comp == "=":
            if args["obj1"] == args["obj2"]:
                valid = True
        elif comp == "!":
            if args["obj1"] != args["obj2"]:
                valid = True
        elif comp == ">":
            if args["obj1"] > args["obj2"]:
                valid = True
        elif comp == "<":
            if args["obj1"] < args["obj2"]:
                valid = True

    return valid

def varInter(args):
    assignMode = args["mode"]

    currentValue = memory.getVar(args["name"])
    if currentValue is None:
        memory.setVar(args["name"], 0)
        currentValue = 0

    if assignMode == "=" or assignMode == "is" or assignMode == "":
        memory.setVar(args["name"], args["value"])
    elif assignMode == "+":
        memory.setVar(args["name"], currentValue + args["value"])
    elif assignMode == "-":
        memory.setVar(args["name"], currentValue - args["value"])
    elif assignMode == "*":
        memory.setVar(args["name"], currentValue * args["value"])
    elif assignMode == "/":
        memory.setVar(args["name"], currentValue / args["value"])
    elif assignMode == "%":
        memory.setVar(args["name"], currentValue % args["value"])
    elif assignMode == "**":
        memory.setVar(args["name"], currentValue ** args["value"])

def printInter(args):
    consoleValue = memory.getVar("console") or ""
    memory.setVar("console", consoleValue + "\n" + "  " + str(args["value"]))

def whileInter(args):
    args["ifArgs"]["obj1"] = getValue(args["obj1type"], args["obj1name"])
    args["ifArgs"]["obj2"] = getValue(args["obj2type"], args["obj2name"])
    while ifInter(args["ifArgs"]):
        for i, line in enumerate(args["lines"]):
            runLine(line, currentLine + i)
        args["ifArgs"]["obj1"] = getValue(args["obj1type"], args["obj1name"])
        args["ifArgs"]["obj2"] = getValue(args["obj2type"], args["obj2name"])

def forInter(args):
    for i in range(args["begin"], args["end"], args["step"]):
        memory.setVar(args["variableName"], i)
        for i, line in enumerate(args["lines"]):
            runLine(line, currentLine + i)
    memory.deleteVar(args["variableName"])

def runVar(args):
    varType = args[2]
    value = 0
    if len(args) < 4:
        value = int(args[2])
    elif len(args) > 4:
        value = " ".join(args[3:])
    else:
        value = getValue(varType, args[3])
    
    varInter({
        "name": args[0],
        "mode": args[1],
        "value": value
    })

def runIf(args):
    global currentLine, currentScript, embedCount
    embedCount += 1
    currentLine += 1
    obj1 = getValue(args[0], args[1])
    obj2 = getValue(args[3], args[4])
    if ifInter({
        "obj1": obj1,
        "comp": args[2],
        "obj2": obj2
    }):
        for i, line in enumerate(getFollowingLines()):
            runLine(line, currentLine + i)
    embedCount -= 1
    currentLine -= 1

def runWhile(args):
    global currentLine, currentScript, embedCount
    comp = args[2]
    embedCount += 1
    currentLine += 1
    lines = getFollowingLines()

    newArgs = {
        "ifArgs": {
            "obj1": args[1],
            "comp": comp,
            "obj2": args[4]
        },
        "obj1type": args[0],
        "obj1name": args[1],
        "obj2type": args[3],
        "obj2name": args[4],
        "lines": lines
    }
    whileInter(newArgs)
    currentLine -= 1
    embedCount -= 1

def runFor(args):
    global currentLine, currentScript, embedCount
    embedCount += 1
    currentLine += 1
    lines = getFollowingLines()

    forBounds = args[1].split(",")
    begin = 0
    end = 0
    step = 1
    if len(forBounds) > 1:
        begin = forBounds[0]
        end = forBounds[1]
        if len(forBounds) > 2:
            step = forBounds[2]
    else:
        end = forBounds[0]
    
    begin_val = memory.getVar(begin)
    end_val = memory.getVar(end)
    step_val = memory.getVar(step)
 
    forArgs = {
        "begin": begin_val if begin_val is not None else int(begin),
        "end": end_val if end_val is not None else int(end),
        "step": step_val if step_val is not None else int(step),
        "variableName": args[0],
        "lines": lines
    }

    forArgs = {
        "begin": memory.getVar(begin) or int(begin),
        "end": memory.getVar(end) or int(end),
        "step": memory.getVar(step) or int(step),
        "variableName": args[0],
        "lines": lines
    }
    forInter(forArgs)
    currentLine -= 1
    embedCount -= 1

def runFunc(args):
    global currentLine, currentScript, embedCount
    embedCount += 1
    currentLine += 1
    if not memory.getFunc(args[0]):
        lines = getFollowingLines()
        memory.setFunc(args[0], {
            "lines": lines,
            "startLine": currentLine,
            "script": currentScript
        })
    else:
        func = memory.getFunc(args[0])
        oldScript = currentScript
        currentScript = func["script"]
        for i, line in enumerate(func["lines"]):
            runLine(line, func["startLine"] + i)
        currentScript = oldScript
    embedCount -= 1
    currentLine -= 1

def runImport(args):
    global currentLine, currentScript
    oldScript = currentScript
    oldLine = currentLine
    moduleName = args[0] + ".txt"
    if not os.path.exists(moduleName): return
    with open(moduleName, "r") as f:
        text = f.read()
        lines = text.split("\n")
        currentScript = lines
        currentLine = 0
        for i, line in enumerate(lines):
            runLine(line, i)
    currentScript = oldScript
    currentLine = oldLine

def runLine(line, lineIndex):
    global currentLine
    currentLine = lineIndex
    args = line.split(" ")
    #print("Running line:", line)

    if not args or line.startswith("- ") or line.startswith("#") or args[0] == "":
        return
    
    if args[0] == "var":
        runVar(args[1:])
    elif args[0] == "if":
        runIf(args[1:])
    elif args[0] == "print":
        value = memory.getVar(args[1])
        if value == None: value = " ".join(args[1:])
        printInter({
            "value": value
        })
    elif args[0] == "while":
        runWhile(args[1:])
    elif args[0] == "for":
        runFor(args[1:])
    elif args[0] == "func":
        runFunc(args[1:])
    elif args[0] == "import":
        runImport(args[1:])
    else:
        runVar(args)
