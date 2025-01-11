''' Advent of code 2019 Day 5 - Sunny with a Chance of Asteroids'''

import os

INPUT_FILE=__file__.replace('.py', '.dat')

def to_number(digits: list) -> int:
    return int(''.join(map(str, digits)))

def to_list(number: int) -> list:
    return [int(i) for i in str(number)]

def get_modes(instruction: int, parameter_count: int = 3) -> list:
    params = instruction // 100
    string = str(params).zfill(parameter_count)
    return list(reversed(to_list(string)))

# For part 1
def run_program(code: list, inputs: list) -> int:
    code = code[:]
    output = 0
    pos = 0

    while (code[pos] % 100) != 99:
        instruction = code[pos + 0]
        params = [code[pos + 1], code[pos + 2], code[pos + 3]]

        operation = instruction % 100
        modes = get_modes(instruction)

        values = [0] * 2
        # Addition
        if operation == 1:
            for i in range(2):
                if modes[i] == 0:
                    values[i] = code[params[i]]
                else:
                    values[i] = params[i]

            code[params[2]] = values[0] + values[1]
            pos += 4

        # Multiplication
        elif operation == 2:
            for i in range(2):
                if modes[i] == 0:
                    values[i] = code[params[i]]
                else:
                    values[i] = params[i]

            code[params[2]] = values[0] * values[1]
            pos += 4

        # Store input
        elif operation == 3:
            value = inputs[0]
            inputs = inputs[1:]
            code[params[0]] = value
            pos += 2
        
        # Get output
        elif operation == 4:
            for i in range(1):
                if modes[i] == 0:
                    values[i] = code[params[i]]
                else:
                    values[i] = params[i]

            output = values[0]
            pos += 2

        # Jump if true
        elif operation == 5:
            for i in range(2):
                if modes[i] == 0:
                    values[i] = code[params[i]]
                else:
                    values[i] = params[i]

            if values[0] != 0:
                pos = values[1]
            else:
                pos += 3

        # Jump if false
        elif operation == 6:
            for i in range(2):
                if modes[i] == 0:
                    values[i] = code[params[i]]
                else:
                    values[i] = params[i]

            if values[0] == 0:
                pos = values[1]
            else:
                pos += 3

        # Less than
        elif operation == 7:
            for i in range(2):
                if modes[i] == 0:
                    values[i] = code[params[i]]
                else:
                    values[i] = params[i]

            if values[0] < values[1]:
                code[params[2]] = 1
            else:
                code[params[2]] = 0
            pos += 4

        # Equals
        elif operation == 8:
            for i in range(2):
                if modes[i] == 0:
                    values[i] = code[params[i]]
                else:
                    values[i] = params[i]

            if values[0] == values[1]:
                code[params[2]] = 1
            else:
                code[params[2]] = 0
            pos += 4

        else:
            raise RuntimeError(f"error in operation: {pos}")

    return code, output

# For part 1 and 2
def edit_memory(code: list, noun = 12, verb = 2) -> list:
    return [code[0], noun, verb, *code[3:]]

# Part 1 asserts
assert(run_program([1,0,0,0,99], [1])[0] == [2,0,0,0,99])
assert(run_program([2,3,0,3,99], [1])[0] == [2,3,0,6,99])
assert(run_program([2,4,4,5,99,0], [1])[0] == [2,4,4,5,99,9801])
assert(run_program([1,1,1,4,99,5,6,0,99], [1])[0] == [30,1,1,4,2,5,6,0,99])

# Part 1 solution
with open(INPUT_FILE, 'r') as f:
    intcode = list(map(int, f.read().split(",")))
    end_code, output = run_program(intcode, [1])

    print(f"Part 1: {output}")


# Part 2 asserts
assert run_program([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], inputs = [0])[1] == 0

assert run_program([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9], inputs = [1])[1] == 1

assert run_program([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], inputs = [0])[1] == 0

assert run_program([3,3,1105,-1,9,1101,0,0,12,4,12,99,1], inputs = [1])[1] == 1

assert run_program([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], inputs = [0])[1] == 999

assert run_program([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], inputs = [7])[1] == 999

assert run_program([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], inputs = [8])[1] == 1000

assert run_program([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], inputs = [9])[1] == 1001

assert run_program([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99], inputs = [20])[1] == 1001

# Part 2 solution
end_code, output = run_program(intcode, inputs=[5])
print(f"Part 2: {output}")