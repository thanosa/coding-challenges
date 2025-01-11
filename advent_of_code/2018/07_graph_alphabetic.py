import fileinput
import time
import re

from collections import defaultdict

INPUT_FILE = "aoc_2018_07.dat"

start = time.time()

inputs = [re.findall(r' ([A-Z]) ', x) for x in list(fileinput.input(INPUT_FILE))]

# Data structures
depends = defaultdict(set)
tasks = set()
for pred, succ in inputs:
    depends[succ].add(pred)
    tasks |= {pred, succ}

# Searching
done = []
for _ in tasks:
    done.append(min(x for x in tasks if x not in done and depends[x] <= set(done)))
result = ''.join(done)

print("Part1: The result is: ", result)

done = set()
seconds = 0
counts = [0] * 5
work = [''] * 5

while True:
    for i, count in enumerate(counts):
        if count == 1:
            done.add(work[i])
        counts[i] = max(0, count - 1)

    while 0 in counts:
        i = counts.index(0)
        candidates = [x for x in tasks if depends[x] <= done]
        if not candidates:
            break
        task = min(candidates)
        tasks.remove(task)

        counts[i] = ord(task) - ord('A') + 61
        work[i] = task

    if sum(counts) == 0:
        break
    seconds += 1

result = seconds

print("Part2: The result is: ", result)
print("Seconds spent: ", round(time.time() - start, 5))
