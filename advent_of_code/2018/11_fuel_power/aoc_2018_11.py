import time
import fileinput
import re
import math


INPUT_FILE = "aoc_2018_11.dat"
start = time.time()


def solve(_x, _y, _serial) -> int:
    rack_id = _x + 10
    power_level = ((rack_id * _y) + _serial) * rack_id
    if power_level < 100:
        hundreds = 0
    else:
        hundreds = int(str(power_level)[-3])
    return hundreds - 5

assert solve(122, 79, 57) == -5
assert solve(217, 196, 39) == 0
assert solve(101, 153, 71) == 4


serial = 9995

matrix = [[solve(x, y, serial) for x in range(300)] for y in range(300)]

grid_size = 300
max_total = -math.inf
max_x = -1
max_y = -1

for window_size in range(1, grid_size + 1):
    for y in range(0, grid_size - window_size + 1):
        for x in range(0, grid_size - window_size + 1):
            total = 0
            for iy in range(window_size):
                for ix in range(window_size):
                    total += matrix[y + iy][x + ix]
            if total > max_total:
                max_total = total
                max_x = x
                max_y = y

result = (max_x, max_y)
print("Part1: The result is: ", result)


result = 0
print("Part2: The result is: ", result)
print("Seconds spent: ", round(time.time() - start, 5))
