import time
import fileinput
from collections import defaultdict


INPUT_FILE = "aoc_2018_12.dat"
start = time.time()

lines = list(fileinput.input(INPUT_FILE))

init_state = set(i for i, x in enumerate(lines[0].split()[-1]) if x == "#")

rules = dict(line.split()[::2] for line in lines[2:])


def step(state):
    result = set()

    for i in range(min(state) - 2, max(state) + 3):
        w = ''.join('#' if j in state else '.' for j in range(i-2, i+3))
        if rules[w] == '#':
            result.add(i)
    return result

s = init_state

for _ in range(20):
    s = step(s)

res = sum(s)

print("Part1: The result is: ", res)

# part 2
s = init_state
p = n = 0
# run enough iterations, tracking current and previous sums
for i in range(1000):
    p = n
    s = step(s)
    n = sum(s)
# extrapolate to 50 billion
res = (p + (n - p) * (50000000000 - i))

print("Part2: The result is: ", res)
print("Seconds spent: ", round(time.time() - start, 5))
