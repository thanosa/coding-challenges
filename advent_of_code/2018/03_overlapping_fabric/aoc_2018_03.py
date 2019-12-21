import fileinput
import time
import re

from collections import defaultdict

INPUT_FILE = "aoc_2018_03.dat"

start = time.time()

inputs = defaultdict(set)
for line in fileinput.input(INPUT_FILE):
    _id, x, y, w, h = map(int, re.findall(r'\d+', line))
    for j in range(y, y + h):
        for i in range(x, x + w):
            inputs[(i, j)].add(_id)

result = sum(len(x) > 1 for x in inputs.values())

print("Part1: The result is: ", result)

all_ids = set()
invalid_ids = set()
for x in inputs.values():
    all_ids |= x
    if len(x) > 1:
        invalid_ids |= x

result = next(iter(all_ids - invalid_ids))

print("Part2: The result is: ", result)
print("Seconds spent: ", round(time.time() - start, 5))
