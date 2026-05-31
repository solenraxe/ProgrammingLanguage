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

def runLine(line):
    args = line.split(" ")
    if not args:
        return
    
    lineInter = args[0] + "Inter"
    
