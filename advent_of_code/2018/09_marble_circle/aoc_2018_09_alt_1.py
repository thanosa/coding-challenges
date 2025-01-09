import time
import fileinput
import re

from collections import deque


def solve(_num_players, _num_marbles):
    # initialize a double-ended queue with zero
    d = deque([0])
    # track score for each player
    scores = [0] * _num_players
    for m in range(1, _num_marbles + 1):
        if m % 23 == 0:
            d.rotate(7)
            scores[m % _num_players] += m + d.pop()
            d.rotate(-1)
        else:
            d.rotate(-1)
            d.append(m)
    return max(scores)


assert solve(9, 25) == 32
assert solve(10, 1618) == 8317
assert solve(13, 7999) == 146373
assert solve(17, 1104) == 2764
assert solve(21, 6111) == 54718
assert solve(30, 5807) == 37305


INPUT_FILE = "aoc_2018_09.dat"
start = time.time()

num_players, num_marbles = map(int, re.findall(r'\d+', next(fileinput.input(INPUT_FILE))))

result = solve(num_players, num_marbles)
print("Part1: The result is: ", result)


result = solve(num_players, num_marbles * 100)
print("Part2: The result is: ", result)
print("Seconds spent: ", round(time.time() - start, 5))
