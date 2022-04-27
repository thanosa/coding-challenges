'''

https://www.codingame.com/training/easy/offset-arrays

'''


import sys

from typing import List


def debug(message):
    print(message, file=sys.stderr, flush=True)

# Read meta data
n = int(input())

arrays = {}
for i in range(n):
    assignment = input()

    # Retrieve the inputs
    LHS, RHS = [side.strip() for side in assignment.split("=")]

    name = LHS.split('[')[0]
    index = int(LHS.split('[')[1].split('..')[0])
    values = [int(v) for v in RHS.split()]

    arrays[name] = {
        "index": index,
        "values": values
    }


# Parse the request
r = input().split('[')
r[-1] = int(r[-1].split(']')[0])

while len(r) > 1:
    temp_name = r[-2]
    temp_index = r[-1]

    array = arrays[temp_name]

    array_index = array["index"]
    array_values = array["values"]

    real_index = (-1 * array_index) + temp_index

    # Update the 2nd from last with the value and remove the last
    r[-2] = array_values[real_index]
    del r[-1]

print(r[0])
