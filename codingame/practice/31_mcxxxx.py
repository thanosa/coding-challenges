'''

https://www.codingame.com/training/medium/mcxxxx-microcontroller-simulation

'''


import sys


def debug(message):
    print(message, file=sys.stderr, flush=True)


def cap(value):
    # Cap the value to the register limits
    return max(min(value, 999), -999)

def isint(value):
    is_positive_int = value.isdigit()
    is_negative_int = value[0] == '-' and value[1:].isdigit()
    return is_positive_int or is_negative_int

# Read the puzzle inputs
k = int(input())
data = list(map(int, input().split()))
n = int(input())
code = [list(map(str, input().split())) for i in range(n)]

# Parse the labels
labels = {}
for line_number, statement in enumerate(code):
    arg0 = statement[0]
    if arg0[-1] == ":":
        label = arg0[:-1]
        # Store the label number
        labels[label] = line_number
        # Remove the label from the statement
        code[line_number].pop(0)

# Initialization of global storage
registers = {"acc": 0, "dat": 0}
outputs = []
cursor = 0

# Initilazation of test state
is_test_oper = is_test_tcp = False
test_oper_enabled = False
plus_enabled = minus_enabled = False


# Main execution
while True:
    if cursor == len(code):
        break
    
    statement = code[cursor]
    
    # Empty statements are skipped
    if len(statement) == 0:
        cursor += 1
        continue

    # Comments are skipped
    command = statement[0]
    if command == "#":
        cursor += 1
        continue

    # Commands with @ should be executed once
    if command == "@":
        statement.pop(0)
        command = statement[0]

        # Make sure the code will not be executed again
        code[cursor][0] = "#"
     
    # Initialization on command specifics
    value = arg = 0

    # Read the conditional execution
    if command in ["+", "-"]:
        if is_test_oper:
            if (test_oper_enabled and command == "+") or (not test_oper_enabled and command == "-"):
                statement = statement [1:]
                command = statement[0]
            else:
                cursor += 1
                continue
  
        elif is_test_tcp:
            if (command == "+" and plus_enabled) or (command == '-' and minus_enabled):
                statement = statement [1:]
                command = statement[0]
            else:
                cursor += 1
                continue
        else:
            cursor += 1
            continue

    # Execute the command
    if command in ["mov", "add", "sub", "mul"]:
        if len(statement) > 1:
            a0 = statement[1]
            value = data.pop(0) if a0 == "x0" else int(a0) if isint(a0) else registers[a0]

        if len(statement) > 2:
            arg = statement[2] if len(statement) == 3 else None

        if command == "mov":
            if arg == "x1":
                outputs.append(value)
            else:
                registers[arg] = cap(value)

        else:
            if command == "add":
                registers["acc"] = cap(registers["acc"] + value)

            elif command == "sub":
                registers["acc"] = cap(registers["acc"] - value)

            elif command == "mul":
                registers["acc"] = cap(registers["acc"] * value)

    elif command == "not":
        registers["acc"] = 100 if registers["acc"] == 0 else 0

    elif command == "jmp":
        label = statement[1]
        cursor = labels[label]
        continue

    elif command in ["teq", "tgt", "tlt"]:
        is_test_oper = True
        is_test_tcp = False

        arg0 = int(statement[1]) if isint(statement[1]) else registers[statement[1]]
        arg1 = int(statement[2]) if isint(statement[2]) else registers[statement[2]]
        if command == "teq":
            test_oper_enabled = arg0 == arg1

        elif command == "tgt":
            test_oper_enabled = arg0 > arg1
        
        elif command == "tlt":
            test_oper_enabled = arg0 < arg1

    elif command == "tcp":
        is_test_oper = False
        is_test_tcp = True

        arg0 = int(statement[1]) if isint(statement[1]) else registers[statement[1]]
        arg1 = int(statement[2]) if isint(statement[2]) else registers[statement[2]]
        if arg0 > arg1:
            plus_enabled = True
            minus_enabled = False
        elif arg0 == arg1:
            plus_enabled = False
            minus_enabled = False
        elif arg0 < arg1:
            plus_enabled = False
            minus_enabled = True

    elif command == "dgt":
        arg0 = int(statement[1]) if isint(statement[1]) else registers[statement[1]]
        index = int(arg0)
        isolated_digit = int(str(registers["acc"]).zfill(3)[::-1][index])
        registers["acc"] = isolated_digit

    elif command == "dst":
        arg0 = int(statement[1]) if isint(statement[1]) else registers[statement[1]]
        arg1 = int(statement[2]) if isint(statement[2]) else registers[statement[2]]

        index = int(arg0)
        new_digit = str(arg1)
        old_number = str(registers["acc"]).zfill(3)[::-1]
        registers["acc"] = int((old_number[:index] + new_digit + old_number[index + 1:])[::-1])

    cursor += 1
    
# print out the result
print(" ".join(list(map(str, outputs))))