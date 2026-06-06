global vars, funcs
vars = {"console": "Console :"}
funcs = {}

def setVar(name, value):
    vars[name] = value

def getVar(name):
    return vars.get(name)

def deleteVar(name):
    if name in vars:
        del vars[name]

def setFunc(name, value):
    funcs[name] = value

def getFunc(name):
    return funcs.get(name)

def deleteFunc(name):
    if name in funcs:
        del funcs[name]

def clear():
    global vars, funcs
    oldConsole = getVar("console")
    vars = {"console": oldConsole}
    funcs = {}