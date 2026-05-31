from pyxel import line

import variablesMemory as vars

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

    currentValue = vars.getVar(args["name"])
    if currentValue is None:
        vars.setVar(args["name"], 0)
        currentValue = 0

    if assignMode == "=" or assignMode == "is" or assignMode == "":
        vars.setVar(args["name"], args["value"])
    elif assignMode == "+":
        vars.setVar(args["name"], currentValue + args["value"])
    elif assignMode == "-":
        vars.setVar(args["name"], currentValue - args["value"])
    elif assignMode == "*":
        vars.setVar(args["name"], currentValue * args["value"])
    elif assignMode == "/":
        vars.setVar(args["name"], currentValue / args["value"])
    elif assignMode == "%":
        vars.setVar(args["name"], currentValue % args["value"])
    elif assignMode == "**":
        vars.setVar(args["name"], currentValue ** args["value"])

def printInter(args):
    consoleValue = vars.getVar("console") or ""
    vars.setVar("console", consoleValue + "\n" + str(args["value"]))

def whileInter(args):
    while ifInter(args["ifArgs"]):
        args["ifArgs"]["obj1"] = vars.getVar(args["ifArgs"]["obj1"]) or int(args["ifArgs"]["obj1"])
        args["ifArgs"]["obj2"] = vars.getVar(args["ifArgs"]["obj2"]) or int(args["ifArgs"]["obj2"])
        runLine(args["line"])

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
        value = vars.getVar(args[3]) or 0
    varInter({
        "name": args[0],
        "mode": args[1],
        "value": value
    })

def runIf(args):
    obj1 = vars.getVar(args[0]) or int(args[0])
    obj2 = vars.getVar(args[2]) or int(args[2])
    if ifInter({
        "obj1": obj1,
        "comp": args[1],
        "obj2": obj2
    }):
        args = args[3:]
        runLine(" ".join(args))

def runWhile(args):
    obj1 = vars.getVar(args[0]) or int(args[0])
    obj2 = vars.getVar(args[2]) or int(args[2])
    comp = args[1]
    newArgs = {
        "ifArgs": {
            "obj1": obj1,
            "comp": comp,
            "obj2": obj2
        },
        "line": " ".join(args[3:])
    }
    whileInter(newArgs)

def runLine(line):
    args = line.split(" ")
    print("Running line:", line)

    if not args:
        return
    
    if args[0] == "var":
        runVar(args[1:])
    elif args[0] == "if":
        runIf(args[1:])
    elif args[0] == "print":
        value = vars.getVar(args[1]) or " ".join(args[1:])
        printInter({
            "value": value
        })
    elif args[0] == "while":
        runWhile(args[1:])
    else:
        runVar(args)