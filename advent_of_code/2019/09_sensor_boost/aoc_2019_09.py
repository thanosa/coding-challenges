''' Advent of code 2019 Day 9: Sensor Boost '''

INPUT_FILE=__file__.replace('.py', '.dat')

def to_number(digits: list) -> int:
    return int(''.join(map(str, digits)))

def to_list(number: int) -> list:
    return [int(i) for i in str(number)]

def get_modes(instruction: int, parameter_count: int = 3) -> list:
    params = instruction // 100
    string = str(params).zfill(parameter_count)
    return list(reversed(to_list(string)))

def get_dict(lst: list):
    return {k: v for k,v in enumerate(lst)}

def get_value(code: dict, key: int):
    if key in code:
        return code[key]
    else:
        return 0


def run_program(code: dict, inputs: list) -> int:
    code = code.copy()
    output = 0
    pos = 0
    base = 0

    counter = 0
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
                    values[i] = get_value(code, params[i])
                elif modes[i] == 1:
                    values[i] = params[i]
                elif modes[i] == 2:
                    values[i] = get_value(code, params[i] + base)

            if modes[2] == 0:
                code[params[2]] = values[0] + values[1]
            else:
                code[params[2] + base] = values[0] + values[1]
            pos += 4

        # Multiplication
        elif operation == 2:
            for i in range(2):
                if modes[i] == 0:
                    values[i] = get_value(code, params[i])
                elif modes[i] == 1:
                    values[i] = params[i]
                elif modes[i] == 2:
                    values[i] = get_value(code, params[i] + base)

            if modes[2] == 0:
                code[params[2]] = values[0] * values[1]
            else:
                code[params[2] + base] = values[0] * values[1]
            pos += 4

        # Store input
        elif operation == 3:
            if modes[0] == 0:
                code[params[0]] = inputs.pop(0)
            elif modes[0] == 2:
                code[params[0] + base] = inputs.pop(0)
            else:
                raise RuntimeError("fail")

            pos += 2
        
        # Get output
        elif operation == 4:
            if modes[0] == 0:
                values[0] = get_value(code, params[0])
            elif modes[0] == 1:
                values[0] = params[0]
            elif modes[0] == 2:
                values[0] = get_value(code, params[0] + base)

            yield values[0]
            pos += 2

        # Jump if true
        elif operation == 5:
            for i in range(2):
                if modes[i] == 0:
                    values[i] = get_value(code, params[i])
                elif modes[i] == 1:
                    values[i] = params[i]
                elif modes[i] == 2:
                    values[i] = get_value(code, params[i] + base)

            if values[0] != 0:
                pos = values[1]
            else:
                pos += 3

        # Jump if false
        elif operation == 6:
            for i in range(2):
                if modes[i] == 0:
                    values[i] = get_value(code, params[i])
                elif modes[i] == 1:
                    values[i] = params[i]
                elif modes[i] == 2:
                    values[i] = get_value(code, params[i] + base)

            if values[0] == 0:
                pos = values[1]
            else:
                pos += 3

        # Less than
        elif operation == 7:
            for i in range(2):
                if modes[i] == 0:
                    values[i] = get_value(code, params[i])
                elif modes[i] == 1:
                    values[i] = params[i]
                elif modes[i] == 2:
                    values[i] = get_value(code, params[i] + base)

            if values[0] < values[1]:
                if modes[2] == 0:
                    code[params[2]] = 1
                else:
                    code[params[2] + base] = 1
            else:
                if modes[2] == 0:
                    code[params[2]] = 0
                else:
                    code[params[2] + base] = 0
            pos += 4

        # Equals
        elif operation == 8:
            for i in range(2):
                if modes[i] == 0:
                    values[i] = get_value(code, params[i])
                elif modes[i] == 1:
                    values[i] = params[i]
                elif modes[i] == 2:
                    values[i] = get_value(code, params[i] + base)

            if values[0] == values[1]:
                if modes[2] == 0:
                    code[params[2]] = 1
                else:
                    code[params[2] + base] = 1
            else:
                if modes[2] == 0:
                    code[params[2]] = 0
                else:
                    code[params[2] + base] = 0
            pos += 4

        # Relative base shift
        elif operation == 9:
            i = 0
            if modes[i] == 0:
                values[i] = get_value(code, params[i])
            elif modes[i] == 1:
                values[i] = params[i]
            elif modes[i] == 2:
                values[i] = get_value(code, params[i] + base)
            base += values[i]
            pos += 2

        else:
            raise RuntimeError(f"error in operation: {pos}")


# Part 1 asserts
input_list = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
output = list(run_program(get_dict(input_list), None))
assert output == input_list

input_list = [1102,34915192,34915192,7,4,7,99,0]
output = list(run_program(get_dict(input_list), None))
assert len(str(output[0])) == 16

input_list = [104,1125899906842624,99]
output = list(run_program(get_dict(input_list), None))
assert output[0] == input_list[1]


# Read the input
with open(INPUT_FILE) as f:
    input_dict = get_dict(list(map(int, f.read().strip().split(','))))
    
# Part 1 solution
result1 = list(run_program(input_dict, [1]))[0]
print(f"Part 1: {result1}")

# Part 2 solution
result2 = list(run_program(input_dict, [2]))[0]
print(f"Part 2: {result2}")

