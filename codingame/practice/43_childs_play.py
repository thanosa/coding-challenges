'''

https://www.codingame.com/ide/puzzle/a-childs-play

'''

import sys


def debug(message):
    print(message, file=sys.stderr, flush=True)


def add_tuples(t1: tuple, t2: tuple) -> tuple:
    """Adds two tuples element-wise"""
    return tuple(map(sum, zip(t1, t2)))


def move(me, direction, obstacles) -> tuple:

    deltas = {
        0: (-1, 0),
        1: (0, +1),
        2: (+1, 0),
        3: (0, -1),
    }

    while True:
        # Move me by delta depending on the direction
        new = add_tuples(me, deltas[direction])

        # If the new location is not an obstacle
        if new not in obstacles:
            return new, direction
        
        # If an obstacle found then turn right
        direction = (direction + 1) % 4


# Constants
OBSTACLE_CHAR = "#"
ME_CHAR = "O"
FREE_CHAR = "."

me = (-1, -1)
direction = 0 # up
obstacles = []

# Read the game inpts
w, h = [int(i) for i in input().split()]
steps = int(input())
debug(f"Steps: {steps}")
for i in range(h):
    line = input()
    debug(line)
    for j, char in enumerate(line):
        if char == OBSTACLE_CHAR:
            obstacles.append((i, j))
        elif char == ME_CHAR:
            me = (i, j)
        elif char == FREE_CHAR:
            pass
        else:
            raise ValueError(char)

debug(f"me: {me}")
debug(f"direction: {direction}")
debug(f"obstacles: {obstacles}")

# Move
final = (-1, -1)
seen = []
for i in range(steps):
    me, direction = move(me, direction, obstacles)
    if (me, direction) not in seen:
        debug(f"me {me} d {direction}  not  in: {seen}")
        seen.append((me, direction))
    else:
        
        loop_length = len(seen)
        reminder = steps % loop_length
        debug(f"seen: {seen}")
        seen.insert(0, seen.pop())
        debug(f"seen: {seen}")
        final = seen[reminder][0]

        debug(f"me {me} d {direction} FOUND in: {seen}")
        debug(f"loop_length: {loop_length}")
        debug(f"steps: {steps}")
        debug(f"reminder: {reminder}")
        debug(f"final: {final}")
        break


print(f"{final[1]} {final[0]}")
