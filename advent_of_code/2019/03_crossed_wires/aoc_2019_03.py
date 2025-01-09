''' Advent of code 2019 Day 3: Crossed Wires'''

import math

INPUT_FILE=__file__.replace('.py', '.dat')

# For part 1
def collect_points(directives: list) -> list:
    current_point = (0, 0)
    points = [current_point]
    for directive in directives:

        gap = directive['length']
        while gap > 0:
            if directive['direction'] == 'U':
                next_point = (current_point[0], current_point[1] + 1)
            elif directive['direction'] == 'D':
                next_point = (current_point[0], current_point[1] - 1)
            if directive['direction'] == 'R':
                next_point = (current_point[0] + 1, current_point[1])
            elif directive['direction'] == 'L':
                next_point = (current_point[0] - 1, current_point[1])
            points.append(next_point)
            current_point = next_point
            gap -= 1
    
    return points

def intersect(lst1, lst2): 
    return list(set(lst1) & set(lst2)) 

def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def calc_wires_points(wires_directives_text: list) -> list:
    wires_directives = []

    for wire_directives in wires_directives_text:
        directive = []
        for point in wire_directives.split(","):
            directive.append({"direction": point[0], "length": int(point[1:])})

        wires_directives.append(directive)

    wires_points = []
    for wire_directives in wires_directives:
        wires_points.append(collect_points(wire_directives))
    
    return wires_points

def calc_min_manhattan_distance(wires_directives_text: list) -> int:
    wires_points = calc_wires_points(wires_directives_text)

    intersections = intersect(wires_points[0], wires_points[1])

    min_distance = math.inf
    for intersection in intersections:
        if intersection != (0,0):
            distance = manhattan((0,0), intersection)
            if distance < min_distance:
                min_distance = distance

    return min_distance

# For part 2
def calc_min_wire_distance(wires_directives_text: list) -> int:
    wires_points = calc_wires_points(wires_directives_text)

    intersections = intersect(wires_points[0], wires_points[1])

    min_distance = math.inf
    for intersection in intersections:
        if intersection != (0,0):
            wire_length = 0
            for wire in wires_points:
                wire_length += wire.index(intersection)

            if wire_length < min_distance:
                min_distance = wire_length

    return min_distance 



# Part 1 asserts
assert(calc_min_manhattan_distance(['R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83']) == 159)
assert(calc_min_manhattan_distance(['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']) == 135)

# Part 1 solution
wires_directives = []
for wire in open(INPUT_FILE):
    wires_directives.append(wire.rstrip())

result1 = calc_min_manhattan_distance(wires_directives)
print(f"Part 1: {result1}")


# Part 2 asserts
assert(calc_min_wire_distance(['R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83']) == 610)
assert(calc_min_wire_distance(['R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7']) == 410)

# Part 2 solution
result2 = calc_min_wire_distance(wires_directives)
print(f"Part 2: {result2}")
