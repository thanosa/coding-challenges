''' Advent of code 2019 Day 2: 1202 Program Alarm'''

import os

INPUT_FILE=__file__.replace('.py', '.dat')

# For part 1
def run_program(code: list) -> int:
    i = 0
    while code[i] != 99:
        operation = code[i + 0]
        address1  = code[i + 1]
        address2  = code[i + 2]
        address3  = code[i + 3]

        if operation == 1:
            code[address3] = code[address1] + code[address2]
        elif operation == 2:
            code[address3] = code[address1] * code[address2]
        elif operation == 99:
            return code
        else:
            raise RuntimeError(f"error in operation: {i}")

        i += 4
    return code

# For part 1 and 2
def edit_memory(code: list, noun = 12, verb = 2) -> list:
    return [code[0], noun, verb, *code[3:]]

# Part 1 asserts
assert(run_program([1,0,0,0,99]) == [2,0,0,0,99])
assert(run_program([2,3,0,3,99]) == [2,3,0,6,99])
assert(run_program([2,4,4,5,99,0]) == [2,4,4,5,99,9801])
assert(run_program([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99])

# Part 1 solution
with open(INPUT_FILE, 'r') as f:
    intcode = list(map(int, f.read().split(",")))
    result = run_program(edit_memory(intcode))[0]

    print(f"Part 1: {result}")

# Part 2 solution
target = 19690720

for noun in range(100):
    for verb in range(100):
        memory = intcode[:]
        check = run_program(edit_memory(memory, noun, verb))[0]

        if check == target:
            result = 100 * noun + verb
            print(f"Part 2: {result}")
