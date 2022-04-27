'''

https://www.codingame.com/training/easy/dungeons-and-maps

'''

import sys
import math


def debug(message):
    print(message, file=sys.stderr, flush=True)


# Read the meta
w, h = [int(i) for i in input().split()]
start_row, start_col = [int(i) for i in input().split()]
n = int(input())

debug(f"There are {n} maps of size: {w}x{h}")
debug(f"You start at: ({start_row}, {start_col})")

# Read the data
maps = []
for i in range(n):
    single_map = []
    for j in range(h):
        single_map.append(list(input()))
    maps.append(single_map)

# Initialze result variables
min_steps = math.inf
best_map = "TRAP"

# Walk the maps one-by-one
for i, single_map in enumerate(maps):
    # Starting position
    x = start_col
    y = start_row

    # Add the starting position in the visited collection
    visited = [(x,y)]

    # Increase the steps
    steps_count = 0

    while True:
        # Read the symbol
        symbol = single_map[y][x]

        # Wall or hole
        if symbol in ['.', '#']:
            break

        # Treasure
        elif symbol == 'T':
            steps_count += 1

            # Is it the best map ?
            if steps_count < min_steps:
                min_steps = steps_count
                best_map = i
            break
        
        # Move
        elif symbol in ['<', '>', '^', 'v']:
            # Move left
            if symbol == '<':
                x += -1
            # Move right
            elif symbol == '>':
                x += 1
            # Move up
            elif symbol == '^':
                y -= 1
            # Move down
            elif symbol == 'v':
                y += 1

            # Increase the steps
            steps_count += 1

            # Check if the new position is valid
            position_is_valid = (0 <= x < w) and (0 <= y < h)
            if not position_is_valid:
                break

            # Check if the new position has been visited in the past
            if (x,y) in visited:
                
                break
            
            # Add the position in the visited collection
            visited.append((x,y))

print(best_map)
