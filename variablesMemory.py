global vars
vars = {"console": "SolPy Console :"}

def setVar(name, value):
    vars[name] = value

def getVar(name):
    return vars.get(name)

def deleteVar(name):
    if name in vars:
        del vars[name]