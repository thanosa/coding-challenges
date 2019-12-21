import time
import fileinput
import re
import math


INPUT_FILE = "aoc_2018_10.dat"
start = time.time()

stars = [list(map(int, x)) for x in [re.findall(r'-*\d+', x) for x in list(fileinput.input(INPUT_FILE))]]

min_area = math.inf
min_stars = None
for loops in range(15000):

    min_x = min(x[0] for x in stars)
    max_x = max(x[0] for x in stars)
    min_y = min(x[1] for x in stars)
    max_y = max(x[1] for x in stars)

    area = (max_x - min_x) * (max_y - min_y)
    if area < min_area:
        min_area = area
        # First run once to find the loop based on min area
        if loops == 10656:
            print(loops, min_area)
            break

    for i, star in enumerate(stars):
        stars[i][0] += star[2]
        stars[i][1] += star[3]

print(min_area)

grid = [['#' if (x, y) in [(star[0], star[1]) for star in stars] else '.'
         for x in range(min_x, max_x + 1)] 
        for y in range(min_y, max_y + 1)]

print("\n".join("".join(row) for row in grid))

result = 0
print("Part1: The result is: ", result)


result = 0
print("Part2: The result is: ", result)
print("Seconds spent: ", round(time.time() - start, 5))
