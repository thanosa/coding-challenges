INPUT_FILE=__file__.replace('.py', '.dat')

# Read the input
with open(INPUT_FILE) as f:
    input_lines = f.read().strip().split('\n')
    
# Part 1 solution
left, right = zip(*[(int(l), int(r)) for l, r in (line.split() for line in input_lines)])
left = list(left)
right = list(right)

result1 = 0
for l, r in zip(sorted(left), sorted(right)):
    result1 += abs(l - r)

print(f"Part 1: {result1}")


# Part 2 solution
left = sorted(left)
right = sorted(right)
i, j = 0, 0
result2 = 0

while i < len(left) and j < len(right):
    if left[i] == right[j]:
        result2 += left[i]
        j += 1
    elif left[i] > right[j]:
        j += 1
    else:
        i += 1
     
print(f"Part 2: {result2}")
