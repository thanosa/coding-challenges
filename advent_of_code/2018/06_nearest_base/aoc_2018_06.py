import fileinput
import time
import re
import math

INPUT_FILE = "aoc_2018_06.dat"

start = time.time()

inputs = list(fileinput.input(INPUT_FILE))
inputs = [re.findall(r'\d+', x) for x in inputs]
inputs = [list(map(int, x)) for x in inputs]


def manhatan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


min_x, min_y = [min(s) for s in zip(*inputs)]
max_x, max_y = [max(s) for s in zip(*inputs)]

nearest_base = {}
exclude_base = set()
safe_region = 0
for x in range(min_x, max_x + 1):
    for y in range(min_y, max_y + 1):
        min_dist = math.inf
        min_base = ""
        has_one_base = True

        total_dist = 0
        boarder_base = (x == min_x) or (x == max_x) or (y == min_y) or (y == max_y)
        for cur_base in inputs:
            cur_dist = manhatan([x, y], cur_base)
            total_dist += cur_dist

            if cur_dist < min_dist:
                min_dist = cur_dist
                min_base = str(cur_base[0]) + "_" + str(cur_base[1])
                has_one_base = True

            elif cur_dist == min_dist:
                has_one_base = False

        if has_one_base:
            if boarder_base:
                exclude_base.add(min_base)

            if min_base not in exclude_base:
                if min_base not in nearest_base:
                    nearest_base[min_base] = 1
                else:
                    nearest_base[min_base] += 1

        if total_dist < 10000:
            safe_region += 1

for base in exclude_base:
    if base in nearest_base:
        del nearest_base[base]

result = str(max(nearest_base.values()))

print("Part1: The result is: ", result)

result = safe_region

print("Part2: The result is: ", result)
print("Seconds spent: ", round(time.time() - start, 5))
