import sys

input = sys.stdin.read().split("\n")[:-1]
commands = []
for i in input:
    commands.append(i.split())

original_list = commands.copy()
noCommands = len(commands)

commands = [i for i in commands if i != []]
noCommands = len(commands)

# for keeping track of line numbers
lineNo = []
num = 1
# sys.stdout.write(original_list)
for i in original_list:
    if i != []:
        if i != [""] and i[0] != "var":
            lineNo.append(num)
    num += 1
# sys.stdout.write(lineNo)
labels = {}
noVars = 0
vars = {}

varFlag = False
varRaiseError = False
varMultiError = False
labelError = False
labelEmptyError = False
gwee = 0
for i in range(len(original_list)):
    if original_list[i] == []: continue
    if original_list[i][0] == "var":
        if varFlag == False:
            if original_list[i][1] not in vars:
                vars[original_list[i][1]] = 0
            else:
                varMultiError = i
                break
        else:
            varRaiseError = i
            break
    elif original_list[i][0][-1] == ":":
        if original_list[i][0][:-1] not in labels:
            if len(original_list[i]) == 1:
                labelEmptyError = gwee
                gwee += 1
                break
            labels[original_list[i][0][:-1]] = gwee
            gwee += 1
        else:
            labelError = i
            break
    else : 
        gwee += 1
        varFlag = True

for i in range(noCommands):
    if commands[i][0][-1] == ":":
        commands[i] = commands[i][1:]

# removing "" from commands
commands = [i for i in commands if i != [""] and i!=[]]
noCommands = len(commands)

# removing vars from commands
commands = [i for i in commands if i[0] != "var"]
noCommands = len(commands)

hltMissingRaiseError = ["hlt"] not in commands
hltRaiseError = commands[-1] != ["hlt"]
hltMultipleRaiseError = False

error = False

if commands.count(["hlt"]) > 1:
    hltMultipleRaiseError = True

zee = 0
for i in vars:
    vars[i] = noCommands+zee
    zee += 1

def decimalToBinary(n):
    b = bin(n).replace('0b', '')
    while len(b) < 8:
        b = '0'+b
    return b

type = [
    {
        "add": "10000",
        "sub": "10001",
        "mul": "10110",
        "xor": "11010",
        "or": "11011",
        "and": "11100",
        "addf": "00000",
        "subf": "00001"
    }, {
        "mov": "10010",
        "rs": "11000",
        "ls": "11001",
        "movf": "00010"
    }, {
        "mov": "10011",
        "div": "10111",
        "not": "11101",
        "cmp": "11110"
    }, {
        "ld": "10100",
        "st": "10101"
    }, {
        "jmp": "11111",
        "jlt": "01100",
        "jgt": "01101",
        "je": "01111"
    }, {
        "hlt": "01010"
    }
]

regMem = {
    "R0": "000",
    "R1": "001",
    "R2": "010",
    "R3": "011",
    "R4": "100",
    "R5": "101",
    "R6": "110",
    "FLAGS": "111"
}

def float_bin(number):
    num, dec = str(number).split(".")
    num = int(num)
    dec = int (dec)
    res = bin(num).lstrip("0b") + "."
    n = "0."+str(dec)
    p, q = n.split(".")
    i = 0
    while(n != "1.0" and i != 5):
        n = str(n)
        p, q = n.split(".")
        n = "0."+q
        n = float(n)
        n *= 2
        n = str(n)
        p, q = n.split(".")
        res += str(p)
        i += 1
    p, q = res.split(".")
    exp = len(p)+2
    res = p[0]+"."+p[1:]+q
    man = (res.split("."))[1]
    man = man[:5]
    exp = bin(exp).lstrip("0b")
    while(len(exp) < 3):
        exp = "0"+exp
    while(len(man) < 5):
        man += "0"
    final = exp+man
    return final

def typeA(command: list):
    if len(command) != 4:
        return ["Error", "General syntax error"]
    out = []
    out.append(type[0][command[0]])
    out.append("00")
    if command[1] not in regMem:
        return ["Error", "Wrong registor name"]
    elif regMem[command[1]] == "111":
        return ["Error", "Illegal flag exception"]
    else:
        out.append(regMem[command[1]])
    if command[2] not in regMem:
        return ["Error", "Wrong registor name"]
    elif regMem[command[2]] == "111":
        return ["Error", "Illegal flag exception"]
    else:
        out.append(regMem[command[2]])
    if command[3] not in regMem:
        return ["Error", "Wrong registor name"]
    elif regMem[command[3]] == "111":
        return ["Error", "Illegal flag exception"]
    else:
        out.append(regMem[command[3]])
    return out

def typeB(command: list):
    if len(command) != 3:
        return ["Error", "General syntax error"]
    out = []
    out.append(type[1][command[0]])
    if command[1] not in regMem:
        return ["Error", "Wrong registor name"]
    elif regMem[command[1]] == "111":
        return ["Error", "Illegal flag exception"]
    else:
        out.append(regMem[command[1]])
    if "." not in command[2][1:]:
        try:
            num = int(command[2][1:])
        except:
            return ["Error", "Invalid immediate value"]
        if num < 0 or num > 255:
            return ["Error", "Illegal immediate value"]
        out.append(decimalToBinary(num))
    else:
        try:
            num = float(command[2][1:])
        except:
            return ["Error", "Invalid immediate value"]
        if num < 0 or num > 255:
            return ["Error", "Illegal immediate value"]
        out.append(float_bin(num))
    return out

def typeC(command: list):
    if len(command) != 3:
        return ["Error", "General syntax error"]
    out = []
    out.append(type[2][command[0]])
    out.append("00000")
    if command[1] not in regMem:
        return ["Error", "Wrong registor name"]
    else:
        out.append(regMem[command[1]])
    if command[2] not in regMem:
        return ["Error", "Wrong registor name"]
    elif regMem[command[2]] == "111":
        return ["Error", "Illegal flag exception"]
    else:
        out.append(regMem[command[2]])
    return out

def typeD(command: list):
    if len(command) != 3:
        return ["Error", "General syntax error"]
    out = []
    out.append(type[3][command[0]])
    if command[1] not in regMem:
        return ["Error", "Wrong registor name"]
    elif regMem[command[1]] == "111":
        return ["Error", "Illegal flag exception"]
    else:
        out.append(regMem[command[1]])
    if command[2] in vars:
        out.append(decimalToBinary(vars[command[2]]))
        return out
    else:
        return ["Error", "Use of undefined variable"]

def typeE(command: list):
    if len(command) != 2:
        return ["Error", "General syntax error"]
    out = []
    out.append(type[4][command[0]])
    out.append("000")
    if command[1] in labels:
        out.append(decimalToBinary(labels[command[1]]))
        return out
    else:
        return ["Error", "Use of undefined label"]

def typeF(command: list):
    if len(command) != 1:
        return ["Error", "General syntax error"]
    else:
        return ["01010","00000000000"]

output = []

wee = 0 
for i in commands:
    # sys.stdout.write(wee, lineNo[wee], i)
    pc = lineNo[wee]
    wee += 1
    if varRaiseError != False:
        error = True
        sys.stdout.write(f"Error @Line{varRaiseError+1}: Variables must be defined at the very beginning")
        break
    if varMultiError != False:
        error = True
        sys.stdout.write(f"Error @Line{varMultiError+1}: Duplicate variable found")
        break
    if labelError != False:
        error = True
        sys.stdout.write(f"Error @Line{labelError+1}: Duplicate label found")
        break
    if labelEmptyError != False:
        error = True
        sys.stdout.write(f"Error @Line{labelEmptyError+1}: Empty label body found")
        break
    if hltMissingRaiseError:
        error = True
        sys.stdout.write(f"Error @Line{len(original_list)}: Missing hlt instruction")
        break
    if hltRaiseError:
        error = True
        sys.stdout.write(f"Error @Line{len(original_list)}: Hlt not being used as the last instruction")
        break
    if hltMultipleRaiseError:
        error = True
        sys.stdout.write(f"Error @Line{len(original_list)}: Multiple hlt instructions not allowed")
        break
    if i[0] in type[0]:
        out = typeA(i)
        if out[0] == "Error":
            error = True
            sys.stdout.write(f"Error @Line{pc}: "+out[1])
            break
        else:
            output.append("".join(out))
    elif i[0] == "mov":
        if len(i) != 3:
            error = True
            sys.stdout.write(f"Error @Line{pc}: General syntax error")
            break
        if i[2][0] == "$":
            out = typeB(i)
            if out[0] == "Error":
                error = True
                sys.stdout.write(f"Error @Line{pc}: "+out[1])
                break
            else:
                output.append("".join(out))
        elif i[2] in regMem:
            out = typeC(i)
            if out[0] == "Error":
                error = True
                sys.stdout.write(f"Error @Line{pc}: "+out[1])
                break
            else:
                output.append("".join(out))
        else:
            error = True
            sys.stdout.write(f"Error @Line{pc}: Wrong Syntax")
            break
    elif i[0] in type[1]:
        out = typeB(i)
        if out[0] == "Error":
            error = True
            sys.stdout.write(f"Error @Line{pc}: "+out[1])
            break
        else:
            output.append("".join(out))
    elif i[0] in type[2]:
        out = typeC(i)
        if out[0] == "Error":
            error = True
            sys.stdout.write(f"Error @Line{pc}: "+out[1])
            break
        else:
            output.append("".join(out))
    elif i[0] in type[3]:
        out = typeD(i)
        if out[0] == "Error":
            error = True
            sys.stdout.write(f"Error @Line{pc}: "+out[1])
            break
        else:
            output.append("".join(out))
    elif i[0] in type[4]:
        out = typeE(i)
        if out[0] == "Error":
            error = True
            sys.stdout.write(f"Error @Line{pc}: "+out[1])
            break
        else:
            output.append("".join(out))
    elif i[0] in type[5]:
        out = typeF(i)
        if out[0] == "Error":
            error = True
            sys.stdout.write(f"Error @Line{pc}: "+out[1])
            break
        else:
            output.append("".join(out))
    else:
        error = True
        sys.stdout.write(f"Error @Line{pc}: General syntax error")
        break 
    pc += 1

if error == False:
    for i in output:
        sys.stdout.write(i+"\n")
