'''

https://www.codingame.com/training/easy/create-the-longest-sequence-of-1s

'''


b = input()

count = 0
buf = "0"
zeros = []
ones = []

for i in range(len(b)):
    if b[i] == buf:
        count += 1
    else:
        if buf == "0":
            zeros.append(count)
        else:
            ones.append(count)
        count = 1
        buf = b[i]

if buf == "0":
    zeros.append(count)
else:
    ones.append(count)
    

max_ones = 1
for i in range(len(ones)):
    left = 1
    this_zero = zeros[i]

    # Left dead-end (no flip)
    if this_zero == 0:
        left = ones[i]
    
    # Left bridge (good flip)
    elif this_zero == 1:
        left = ones[i] + 1 if i == 0 else ones[i] + 1 + ones[i-1]

    # Left addition (poor flip)
    elif this_zero > 1:
        left = ones[i] + 1

    if left > max_ones:
        max_ones = left

    right = 1
    if i < len(zeros) - 1:
        next_zero = zeros[i+1]
        # Right dead-end (no flip)
        if zeros[i] == 0:
            right = ones[i]
        
        # Right bridge (good flip)
        elif zeros[i] == 1:
            right = ones[i] + 1 if i == 0 else ones[i] + 1 + ones[i-1]

        # Right addition (poor flip)
        elif zeros[i] > 1:
            right = ones[i] + 1

    if right > max_ones:
        max_ones = right

print(max_ones)
