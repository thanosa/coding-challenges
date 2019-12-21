import fileinput
import time

from collections import Counter

INPUT_FILE = "aoc_2018_02.dat"

start = time.time()
inputs = list(fileinput.input(INPUT_FILE))

m2 = 0
m3 = 0
for iid in inputs:
    cnt = Counter(iid)
    m2 += 2 in cnt.values()
    m3 += 3 in cnt.values()

result = m2 * m3

print("Part1: The result is: ", result)


must_break = False
for id1 in inputs:
    for id2 in inputs:
        matching = ''.join(a for a, b in zip(id1, id2) if a == b)
        if len(matching) == len(id1) - 1:
            result = matching
            must_break = True
            break

    if must_break:
        break

print("Part2: The result is: ", result)
print("Seconds spent: ", round(time.time() - start, 5))
