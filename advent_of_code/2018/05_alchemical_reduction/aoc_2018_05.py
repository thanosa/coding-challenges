import fileinput
import math
import re
import time

from string import ascii_lowercase

INPUT_FILE = "aoc_2018_05.dat"

start = time.time()

inputs = next(fileinput.input(INPUT_FILE)).strip()

solution = ['']
for c in inputs:
    if c == solution[-1].swapcase():
        solution.pop()
    else:
        solution.append(c)
result = len(''.join(solution))

print("Part1: The result is: ", result)


min_len = math.inf
for x in ascii_lowercase:
    search = x + x.upper()
    clean = re.sub('[' + search + ']', '', inputs)
    result = ['']

    for c in clean:
        if c == result[-1].swapcase():
            result.pop()
        else:
            result.append(c)

    res = ''.join(result)
    cur_len = len(res)
    if cur_len < min_len:
        min_len = cur_len
        min_res = res

result = len(min_res)

print("Part2: The result is: ", result)
print("Seconds spent: ", round(time.time() - start, 5))
