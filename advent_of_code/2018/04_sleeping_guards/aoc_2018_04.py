import fileinput
import time
import re

from collections import defaultdict
from operator import itemgetter

INPUT_FILE = "aoc_2018_04.dat"

start = time.time()

inputs = sorted(fileinput.input(INPUT_FILE))

totals = defaultdict(int)
minutes = defaultdict(lambda: defaultdict(int))

for line in inputs:
    if '#' in line:
        guard = int(re.search(r'#(\d+)', line).group(1))

    elif 'asleep' in line:
        m0 = int(re.search(r':(\d+)', line).group(1))

    elif 'wakes' in line:
        m1 = int(re.search(r':(\d+)', line).group(1))

        for m in range(m0, m1):
            totals[guard] += 1
            minutes[guard][m] += 1

key = itemgetter(1)
guard = max(totals.items(), key=key)[0]
minute = max(minutes[guard].items(), key=key)[0]
result = guard * minute

print("Guard: ", guard)
print("Minute: ", minute)
print("Part1: The result is: ", result)
print("")


max_times = -1
max_minute = -1
max_guard = -1
for guard, minutes_dic in minutes.items():
    for minute, times in minutes_dic.items():
        cur_times = times
        if cur_times > max_times:
            max_times = cur_times
            max_guard = guard
            max_minute = minute

result = max_guard * max_minute

print("Guard: ", max_guard)
print("minute: ", max_minute)
print("Part2: The result is: ", result)

print("Seconds spent: ", round(time.time() - start, 5))
