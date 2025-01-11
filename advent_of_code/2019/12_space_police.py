''' Advent of code 2019 Day 11 - Space police  '''

from typing import NamedTuple
from enum import Enum

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


class Point(NamedTuple):
    X: int
    Y: int

class Direction(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3


def run_robot(code: dict, start_on_white: bool = False) -> int:
    DIRECTIONS_COUNT = 4

    direction = Direction.UP
    panels = {}
    seen = set()
    color = []
    position = Point(0, 0)
    if start_on_white:
        panels[position] = 1


    finished = False
    brain = run_program(code, color)

    while True:
        try:
            # Sense the color on the point. Default is black (0).
            if position in panels:
                color.append(panels[position])
            else:
                color.append(0)

            paint = next(brain)
            rotation = next(brain)
            if paint == "" or rotation == "":
                raise RuntimeError(f"Failed to read paint: {paint}, rotation: {rotation}")
            
            # Paints the panel.
            panels[position] = paint

            # Keeps track of all visited points.
            seen.add(position)

            # Turn left (0) or right (1).
            if rotation == 0:
                direction = Direction((direction.value + 1) % DIRECTIONS_COUNT)
            elif rotation == 1:
                direction = Direction((direction.value - 1) % DIRECTIONS_COUNT)

            # Move a step forward.
            if direction == Direction.UP:
                position = Point(position.X, position.Y - 1)
            elif direction == Direction.LEFT:
                position = Point(position.X - 1, position.Y)
            elif direction == Direction.DOWN:
                position = Point(position.X, position.Y + 1)
            elif direction == Direction.RIGHT:
                position = Point(position.X + 1, position.Y)
            else:
                raise RuntimeError(f"Wrong direction: {direction}")

        except StopIteration:
            return panels

def print_panels(panels: dict):
    min_x = min(panels, key=lambda panel: panel.X).X
    max_x = max(panels, key=lambda panel: panel.X).X

    min_y = min(panels, key=lambda panel: panel.Y).Y
    max_y = max(panels, key=lambda panel: panel.Y).Y

    print(f"{min_x} {max_x} {min_y} {max_y}")
    for y in range(min_y, max_y + 1):
        row = []
        for x in range(min_x, max_x + 1):
            point = Point(x, y)
            if point in panels:
                if panels[Point(x, y)] == 1:
                    row.append("#")
                else:
                    row.append(" ")
            else:
                row.append(" ")
        print(''.join(row))

# Read the input
with open(INPUT_FILE) as f:
    input_dict = get_dict(list(map(int, f.read().strip().split(','))))
    
# Part 1 solution
panels_count = len(run_robot(input_dict))
print(f"Part 1: {panels_count}")


# Part 2 solution
panels = run_robot(input_dict, True)
print(f"Part 2:")
print_panels(panels)
