'''

https://www.codingame.com/training/easy/equivalent-resistance-circuit-building

'''

import sys
import math


def debug(message):
    print(message, file=sys.stderr, flush=True)


# Read the basic inputs
w, h, t1, t2, t3 = [int(i) for i in input().split()]
debug(f"The map is: {w}x{h}")
debug(f"The times are: {t1}, {t2}, {t3}")

# Initialize
space = dict()

for y in range(h):
    # Read the pictures
    t1_row, t2_row = input().split()

    # Print out the map
    debug(t1_row + " " + t2_row)

    # Calculate the coordinates of the asteroids
    for t, row in enumerate([t1_row, t2_row]):
        for x, e in enumerate(row):
            if e != '.':
                if not e in space:
                    space[e] = dict()
                space[e][t] = ((x, y))

for asteroid in sorted(space.keys()):
    # Coordinates of 1st position
    x1 = space[asteroid][0][0]
    y1 = space[asteroid][0][1]

    # Coordinates of 2nd position
    x2 = space[asteroid][1][0]
    y2 = space[asteroid][1][1]

    # Calculate the horizontal and vertical velocities
    vx = (x2 - x1) / (t2 - t1)
    vy = (y2 - y1) / (t2 - t1)

    # Coordinates of 3rd position
    dt = t3 - t2
    x3 = math.floor((vx * dt) + x2)
    y3 = math.floor((vy * dt) + y2)

    # Check if the 3rd position is within the maps boundaries.
    is_3rd_position_in_map = (0 <= x3 <= (w-1)) and (0 <= y3 <= (h-1))
    
    # Add the position in the space or None if it is outside of it.
    if is_3rd_position_in_map:
        space[asteroid][2] = (x3, y3)

debug("")

# Initialization of the final map
final_map = h * [w * '.']

# We parse the asteroids in reverse alphabetical order to take care
# about those with overlapping positions (depth)
for asteroid, positions in sorted(space.items(), reverse=True):
    # If there is a 3rd position then we need to draw that asteroid
    if 2 in positions:
        x = positions[2][0]
        y = positions[2][1]
        final_map[y] = final_map[y][0:x] + asteroid + final_map[y][x+1:]

# Print out the final map
for row in final_map:
    print(row)
