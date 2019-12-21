''' Advent of code 2019 Day 4: Secure Container'''

import math

INPUT_FILE=__file__.replace('.py', '.dat')

# returns -1 if the digits are fine (not decreasing) 
# otherwise returns the index of the right-most digit that is not ok
def find_issue_digit(digits: list, length: int) -> int:
    pos = length - 1
    while pos > 0:
        if (digits[pos] < digits[pos - 1]):
            return pos
        else:
            pos -= 1
    
    return -1

def has_same(digits: list, length: int) -> bool:
    pos = length - 1
    while pos > 0:
        if (digits[pos] == digits[pos - 1]):
            return True
        pos -= 1
    return False

def fix_digits(digits: list, issue_index: int) -> list:
    if issue_index <= 0 and issue_index != -1:
        raise RuntimeError(f"Wrong issue index {issue_index}")

    fix_number = digits[issue_index - 1]
    for i in range(issue_index, len(digits)):
        digits[i] = fix_number

    return digits

def to_number(digits: list) -> int:
    return int(''.join(map(str, digits)))

def to_list(number: int) -> list:
    return [int(i) for i in str(number)]

def increase(digits: list) -> list:
    return to_list(to_number(digits) + 1)

def has_pair(digits: list, length: int) -> bool:
    pos = length - 1
    while pos > 0:
        if pos == length - 1:
            # Cases X X X 2 1 1
            if (digits[pos] == digits[pos - 1]) and (digits[pos - 1] != digits[pos - 2]):
                return True
        elif pos == 1:
            # Cases 1 1 2 X X X
            if (digits[pos] == digits[pos - 1]) and (digits[pos] != digits[pos + 1]):
                return True
        else:
            # Cases X 1 2 2 1 X
            if (digits[pos] == digits[pos - 1]) and (digits[pos] != digits[pos + 1] and digits[pos - 1] != digits[pos - 2]):
                return True
        pos -= 1
    return False

def count_valid_pwd(lower: list, upper: list) -> int:

    valid_count_part_1 = 0
    valid_count_part_2 = 0
    length = len(upper)

    check_digits = lower
    while to_number(check_digits) < to_number(upper):
        issue_index = find_issue_digit(check_digits, length)

        if issue_index == -1:
            if has_same(check_digits, length):
                valid_count_part_1 += 1
                if has_pair(check_digits, length):
                    valid_count_part_2 += 1
            check_digits = increase(check_digits)
        else:
            check_digits = fix_digits(check_digits, issue_index)

    return valid_count_part_1, valid_count_part_2
    
# Read the range.
pwd_range = []
for line in open(INPUT_FILE):
    pwd_range = list(map(int, line.strip().split("-")))

# Create an array with length as the upper range.
digits = [0] * 2
for i in range(len(pwd_range)):
    digits[i] = to_list(pwd_range[i])

# Part 1 and 2 asserts
assert has_same([5,5,6,4,3,2], 6) == True
assert has_same([5,5,5,5,3,2], 6) == True
assert has_same([5,5,6,6,3,2], 6) == True
assert has_same([5,5,4,4,3,4], 6) == True
assert has_same([1,1,6,4,3,2], 6) == True
assert has_same([1,2,6,4,3,3], 6) == True
assert has_same([1,1,6,4,9,9], 6) == True

assert has_same([1,2,3,4,5,6], 6) == False
assert has_same([1,2,1,2,1,2], 6) == False
assert has_same([6,1,6,4,9,6], 6) == False

assert find_issue_digit([8,7,6,5,4,3], 6) == 5
assert find_issue_digit([8,7,6,5,4,4], 6) == 4
assert find_issue_digit([7,8,7,7,7,7], 6) == 2
assert find_issue_digit([7,6,6,6,6,6], 6) == 1

assert find_issue_digit([7,7,7,7,7,8], 6) == -1
assert find_issue_digit([6,7,7,7,7,7], 6) == -1
assert find_issue_digit([7,7,7,7,7,7], 6) == -1


# Part 2 asserts
assert has_pair([7,7,7,7,7,7], 6) == False
assert has_pair([7,1,7,7,7,7], 6) == False
assert has_pair([1,7,3,7,7,7], 6) == False
assert has_pair([7,1,7,1,7,1], 6) == False
assert has_pair([7,1,7,1,1,1], 6) == False

assert has_pair([7,7,7,7,1,1], 6) == True
assert has_pair([7,7,7,1,1,7], 6) == True
assert has_pair([7,1,1,7,7,7], 6) == True
assert has_pair([1,1,7,7,7,7], 6) == True
assert has_pair([1,1,7,7,2,2], 6) == True

# Part 1 and 2 solution
result1, result2 = count_valid_pwd(digits[0], digits[1])
 
print(f"Part 1: {result1}")
print(f"Part 2: {result2}")
