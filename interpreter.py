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

    if assignMode == "=":
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
    print(args["value"])

def runLine(line):
    args = line.split(" ")
    print("Running line:", line)

    if not args:
        return
    
    if args[0] == "var":
        varType = args[3]
        value = 0
        if len(args) < 5 or varType == "int":
            value = int(args[3])
        elif varType == "str":
            value = args[4]
        elif varType == "bool":
            value = args[4].lower() == "true"
        varInter({
            "name": args[1],
            "mode": args[2],
            "value": value
        })
    elif args[0] == "if":
        obj1 = vars.getVar(args[1]) or int(args[1])
        obj2 = vars.getVar(args[3]) or int(args[3])
        if ifInter({
            "obj1": obj1,
            "comp": args[2],
            "obj2": obj2
        }):
            args = args[4:]
            runLine(" ".join(args))
    elif args[0] == "print":
        value = vars.getVar(args[1]) or args[1]
        printInter({
            "value": value
        })