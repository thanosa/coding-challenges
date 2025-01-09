'''

https://www.codingame.com/ide/puzzle/pirates-treasure

'''

import sys
from typing import List, Any


def debug(message: Any) -> None:
    print(message, file=sys.stderr, flush=True)


def get_neighbors(w: int, h:int, x: int, y: int) -> List[List[int]]:

    # Add all neighbors
    everyone = [
        [x-1, y],
        [x+1, y],
        [x, y-1],
        [x, y+1],
        [x-1, y-1],
        [x+1, y+1],
        [x-1, y+1],
        [x+1, y-1],
    ]

    # Remove those that are out of bounds
    valid = [n for n in everyone if all(num >= 0 for num in n) and n[0] < w and n[1] < h]

    return valid


EMPTY = 0
TREASURE = 1
w = int(input())
h = int(input())
cells = [[int(j) for j in input().split()] for _ in range(h)]


for line in cells:
    debug(line)

for y in range(h):
    for x in range(w):
        if cells[y][x] != EMPTY:
            continue
            
        neighbors = get_neighbors(w, h, x, y)
        values = [cells[n[1]][n[0]] for n in neighbors]
        is_treasure = all(v == TREASURE for v in values)

        if is_treasure:
            print(x, y)
            exit(0)
