''' Advent of code 2019 Day 7: Amplification Circuit'''

from itertools import permutations

INPUT_FILE='aoc_2019_07.dat'


def to_number(digits: list) -> int:
    return int(''.join(map(str, digits)))


def to_list(number: int) -> list:
    return [int(i) for i in str(number)]


def get_modes(instruction: int, parameter_count: int = 3) -> list:
    params = instruction // 100
    string = str(params).zfill(parameter_count)
    return list(reversed(to_list(string)))


def run_program(code: list, inputs: list) -> int:
    code = code[:]
    output = 0
    pos = 0

    while (code[pos] % 100) != 99:
        instruction = code[pos + 0]
        
        params = []
        for i in range(3):
            try:
                param = code[pos + 1 + i]
            except:
                param = None
            params.append(param)

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
            code[params[0]] = inputs.pop(0)
            pos += 2
        
        # Get output
        elif operation == 4:
            for i in range(1):
                if modes[i] == 0:
                    values[i] = code[params[i]]
                else:
                    values[i] = params[i]

            yield values[0]
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


def run_amplifiers(code: list, phases: list):
    first_signal_index = 0
    initial_signal = 0

    # Converts the list, to a list of lists.
    # The first phase is accompanied with the initial signal which is zero.
    inputs = []
    for i, phase in enumerate(phases):
        inputs.append([phase])
    
    inputs[first_signal_index].append(initial_signal)

    # Create a list of generators with their inputs
    generators = [run_program(code, _input) for _input in inputs]

    while True:
        for i, generator in enumerate(generators):
            try:
                signal = next(generator)
            except StopIteration:
                return signal

            # The % with the max causes the loop
            next_index = (i + 1) % len(inputs)
            inputs[next_index].append(signal)


def calc_max_thruster(code: list, phases: list) -> int:
    max_thruster = 0

    for phases_permutation in permutations(phases):
        thruster = run_amplifiers(code, phases_permutation)
        if thruster > max_thruster:
            max_thruster = thruster

    return max_thruster
       

# Part 1 asserts
assert run_amplifiers([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], [4,3,2,1,0]) == 43210
assert run_amplifiers([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0], [0,1,2,3,4]) == 54321
assert run_amplifiers([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], [1,0,4,3,2]) == 65210

assert calc_max_thruster([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0], range(5)) == 43210
assert calc_max_thruster([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0], range(5)) == 54321
assert calc_max_thruster([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0], range(5)) == 65210

# Read the input.
with open(INPUT_FILE) as f:
    input_lines = list(map(int, f.read().strip().split(',')))

# Part 1 solution
result1 = calc_max_thruster(input_lines, range(5))
print(f"Part 1: {result1}")

# Part 2 asserts
assert run_amplifiers([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], [9,8,7,6,5]) == 139629729
assert run_amplifiers([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10], [9,7,8,5,6]) == 18216

# Part 2 solution
result2 = calc_max_thruster(input_lines, range(5, 10))
print(f"Part 2: {result2}")
