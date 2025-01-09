'''

https://www.codingame.com/training/easy/the-river-ii-

'''


def sum_digits(number: int) -> int:
    # Calulate the sum of the digits
    return sum([int(c) for c in str(number)])


def next_number(number: int) -> int:
    # Calculate the next number on the digital river
    return number + sum_digits(number)


def max_step(number: int) -> int:
    # The maximum increase of a step can be found be decreasing
    # the most significant digit by one and the replace the 
    # rest fo the numbers with 9.
    #
    # For example given a number 430492 ..
    # the head is 4, so deacresed by 1 is 3
    # the tail is 30492, so by replacing the digits with 9s it becomes 99999
    # combining the head with the tail we get 399999
    # so the max step that could happen is 3+9+9+9+9+9 = 48
        
    head = int(str(number)[0])
    tail_count = len(str(number)) - 1
    return (head - 1) + (9 * tail_count)


def lower_bound(number: int) -> int:
    # The lowest bound of the window we need to search
    return max(number - max_step(number), 0)


# Tests
assert sum_digits(289734) == 33
assert max_step(67343) == (5 + (9*4))
assert next_number(5123) == 5134
assert lower_bound(347) == 327

# Get the input
n = int(input())

# We could search all the numbers starting from 0,
# however it is not needed since we can skip most of them.
# We chose to search only into the window between our number
# and the maximum increase that can happen in a step 
# calculated by man_inc function
for i in range(lower_bound(n), n):
    if next_number(i) == n:
        print("YES")
        exit(0)
print("NO")
