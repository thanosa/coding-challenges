'''

https://www.codingame.com/training/easy/dungeons-and-maps

'''

import itertools
import sys


def debug(message):
    print(message, file=sys.stderr, flush=True)


def count_repetitive(items, index):
    # Count the repetition to the right of the item under index
    
    i = 1
    while True:
        # If the given index is the last item, the repetition is 1
        if index + 1 == len (items):
            return 1

        if items[index + i] == items[index]:
            i += 1
        else:
            return i


# Read the meta
w, h, count_x, count_y = [int(i) for i in input().split()]

debug(f"Size: {w}x{h}")
debug(f"Counts: {count_x},{count_y}")

# Store the measurements including the boundaries (0 and size) in an ascending order
x_meas = sorted([int(i) for i in input().split()] + [w] + [0])
y_meas = sorted([int(i) for i in input().split()] + [h] + [0])

# Calculate the sizes
x_sizes = sorted([(b-a) for a,b in itertools.combinations(x_meas, 2)])
y_sizes = sorted([(b-a) for a,b in itertools.combinations(y_meas, 2)])

# Getting all combinations between sizes has complexity of n^2 
# so the following cannot work on case "9: Imbalance" for performance reasons
#
# # # print(sum([1 if x == y else 0 for x in x_sizes for y in y_sizes]))

squares_count = 0
i = j = 0
while True:

    # Check if i and j are still within bounds
    if (i == len(x_sizes)) or (j == len(y_sizes)):
        print(squares_count)
        exit(0)

    if x_sizes[i] == y_sizes[j]:
        # Calculate the repetitions of the matching items
        x_repetitions = count_repetitive(x_sizes, i)
        y_repetitions = count_repetitive(y_sizes, j)

        # Caclulate the squares count
        squares_count += x_repetitions * y_repetitions
        
        # Update the indexes accordingly
        i += x_repetitions
        j += y_repetitions
    
    elif x_sizes[i] < y_sizes[j]:
        # Increase the index of the smallest item
        i += 1
    
    elif x_sizes[i] > y_sizes[j]:
        # Increase the index of the smallest item
        j += 1
