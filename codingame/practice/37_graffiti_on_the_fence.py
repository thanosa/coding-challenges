'''

https://www.codingame.com/ide/puzzle/graffiti-on-the-fence

'''


# Read the meta
l = int(input())
n = int(input())

# Collect the painted parts in a list of tuples as: (from, to)
painted = [tuple([int(j) for j in input().split()]) for i in range(n)]

# Sort the array
painted.sort()

i = 0
while True:
    # Loop the elements two by two
    current_part, next_part = painted[i], painted[i+1]
    
    # Is there an overlap ?
    if current_part[1] >= next_part[0]:
        # Merge the overlapped onto the current one,
        # remove the next and do NOT increase the index
        # as there might overlap with the next part
        painted[i] = (current_part[0], max(current_part[1], next_part[1]))
        del(painted[i+1])
    else:
        # Increase the index to check the next two parts
        i += 1

    # Are we done ?
    if i == len(painted) - 1:
        break

# If there are unpainted parts in the begining we add the head point
if painted[0][0] != 0: 
    painted.insert(0, (0, 0))

# If there are unpainted parts in the end, we add the tail point
if painted[-1][1] != l:
    painted.append((l, l))

# Reverse the painted parts to get the unpainted ones.
flat = [e for t in painted for e in t][1:-1]
unpainted = [tuple(flat[i:i+2]) for i in range(0, len(flat), 2)]

# Print out unpainted parts
if not unpainted:
    print("All painted")
else:
    for u in unpainted:
        print(*u)


def calc_distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Calculate the distance between two points"""
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5