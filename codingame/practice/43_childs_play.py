'''

https://www.codingame.com/ide/puzzle/a-childs-play

'''

import sys


def debug(message):
    print(message, file=sys.stderr, flush=True)


def add_tuples(t1: tuple, t2: tuple) -> tuple:
    """Adds two tuples element-wise"""
    return tuple(map(sum, zip(t1, t2)))


def get_preview(me, direction) -> tuple:
    deltas = {
        0: (-1, 0),
        1: (0, +1),
        2: (+1, 0),
        3: (0, -1),
    }

    return add_tuples(me, deltas[direction])


def fix_direction(me: tuple, direction: int, obstacles: list) -> int:
    # If the preview is ok return the direction else turn right
    while True:
        if get_preview(me, direction) not in obstacles:
            return direction

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

debug("map: ")
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

debug(f"")
debug(f"Initial state:")
debug(f"me: ({me} {direction})")
debug(f"obstacles: {obstacles}")
debug(f"steps: {steps}")
debug(f"")

# Initialization
final = (-1, -1)
seen = []

for i in range(steps):

    # Fix the direction
    direction = fix_direction(me, direction, obstacles)

    # Check the position is never seen
    if (me, direction) not in seen:
        seen.append((me, direction))
        me = get_preview(me, direction)
        continue

    debug(f"Loop has been detected at:({me} {direction})")
    debug(f"Squares already seen: {seen}")

    # Locate the loop
    start = 0
    for l, e in enumerate(seen):
        if e == (me, direction):
            start = l
            break
    loop = seen[start:]

    debug(f"The loop starts at: {i}")
    debug(f"The loop has length: {len(loop)}")
    debug(f"The loop is: {loop}")

    remaining_steps = steps - i
    reminder = remaining_steps % len(loop)

    debug(f"The total remaining steps are: {remaining_steps}")
    debug(f"The remaining steps after removing the loops are: {reminder}")
    debug(f"")

    final = loop[reminder][0]
    debug(f"The final square is: {final}")
    break

else:
    debug("No loop has been detected")
    final = me
    debug(f"The final square is: {final}")

print(f"{final[1]} {final[0]}")
