import time
import fileinput
from collections import defaultdict


INPUT_FILE = "aoc_2018_11.dat"
start = time.time()


def summed_area_table(n):
    t = defaultdict(int)
    for y in range(1, 301):
        for x in range(1, 301):
            # compute the value of this cell using the specified formula
            r = x + 10
            p = (((r * y + n) * r) // 100) % 10 - 5
            # store the result in summed-area form
            t[(x, y)] = p + t[(x, y - 1)] + t[(x - 1, y)] - t[(x - 1, y - 1)]
    return t


# derive the sum of this region by checking four corners in the summed-area table
def region_sum(t, s, x, y):
    x0, y0, x1, y1 = x - 1, y - 1, x + s - 1, y + s - 1
    return t[(x0, y0)] + t[(x1, y1)] - t[(x1, y0)] - t[(x0, y1)]


# using the summed-area table `t` and a region size `s` find the sub region with a maximal sum
def best(t, s):
    rs = []
    for y in range(1, 301 - s + 1):
        for x in range(1, 301 - s + 1):
            r = region_sum(t, s, x, y)
            rs.append((r, x, y))
    return max(rs)

# build the summed area table
t = summed_area_table(int(next(fileinput.input(INPUT_FILE))))

# find the best 3x3 region
print('%d,%d' % best(t, 3)[1:])

# find the best region of any size

print('%d,%d,%d' % max(best(t, s) + (s,) for s in range(1, 301))[1:])
print("Seconds spent: ", round(time.time() - start, 5))
