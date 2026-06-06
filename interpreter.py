import memory

global currentLine, currentScript
currentLine = 0
currentScript = []

def getFollowingLines():
    global currentLine, currentScript
    lines = []
    i = 1
    while currentLine + i < len(currentScript) and currentScript[currentLine + i].startswith("- "):
        lines.append(currentScript[currentLine + i][2:])
        i += 1
    return lines

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
    memory.setVar("console", consoleValue + "\n" + str(args["value"]))

def whileInter(args):
    obj1var = memory.getVar(args["ifArgs"]["obj1"]) and args["ifArgs"]["obj1"]
    obj2var = memory.getVar(args["ifArgs"]["obj2"]) and args["ifArgs"]["obj2"]
    if obj1var:
        args["ifArgs"]["obj1"] = memory.getVar(args["ifArgs"]["obj1"])
    if obj2var:
        args["ifArgs"]["obj2"] = memory.getVar(args["ifArgs"]["obj2"])

    while ifInter(args["ifArgs"]):
        if obj1var: args["ifArgs"]["obj1"] = memory.getVar(obj1var)
        if obj2var: args["ifArgs"]["obj2"] = memory.getVar(obj2var)
        for line in args["lines"]:
            runLine(line)

def forInter(args):
    for i in range(args["begin"], args["end"], args["step"]):
        memory.setVar(args["variableName"], i)
        for line in args["lines"]:
            runLine(line)
    memory.deleteVar(args["variableName"])

def runVar(args):
    varType = args[2]
    value = 0
    if len(args) < 4 or varType == "nbr" or varType == "int":
        value = int(args[2])
    elif varType == "txt" or varType == "string":
        value = " ".join(args[3:])
    elif varType == "truth" or varType == "bool":
        value = args[3].lower() == "true"
    elif varType == "var":
        value = memory.getVar(args[3]) or 0
    varInter({
        "name": args[0],
        "mode": args[1],
        "value": value
    })

def runIf(args):
    global currentLine, currentScript
    obj1 = memory.getVar(args[0]) or int(args[0])
    obj2 = memory.getVar(args[2]) or int(args[2])
    if ifInter({
        "obj1": obj1,
        "comp": args[1],
        "obj2": obj2
    }):
        for line in getFollowingLines():
            runLine(line)

def runWhile(args):
    global currentLine, currentScript
    comp = args[1]
    lines = getFollowingLines()

    newArgs = {
        "ifArgs": {
            "obj1": args[0],
            "comp": comp,
            "obj2": args[2]
        },
        "lines": lines
    }
    whileInter(newArgs)

def runFor(args):
    global currentLine, currentScript
    lines = getFollowingLines()

    forArgs = {
        "begin": int(args[1]),
        "end": int(args[2]),
        "step": int(args[3]),
        "variableName": args[0],
        "lines": lines
    }
    forInter(forArgs)

def runFunc(args):
    if not memory.getFunc(args[0]):
        lines = getFollowingLines()
        memory.setFunc(args[0], {
            "lines": lines
        })
    else:
        func = memory.getFunc(args[0])
        for line in func["lines"]:
            runLine(line)

def runLine(line):
    args = line.split(" ")
    #print("Running line:", line)

    if not args or line.startswith("- ") or line.startswith("#") or args[0] == "":
        return
    
    if args[0] == "var":
        runVar(args[1:])
    elif args[0] == "if":
        runIf(args[1:])
    elif args[0] == "print":
        value = memory.getVar(args[1]) or " ".join(args[1:])
        printInter({
            "value": value
        })
    elif args[0] == "while":
        runWhile(args[1:])
    elif args[0] == "for":
        runFor(args[1:])
    elif args[0] == "func":
        runFunc(args[1:])
    else:
        runVar(args)