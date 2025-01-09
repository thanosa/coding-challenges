import re

INPUT_FILE=__file__.replace('.py', '.dat')

with open(INPUT_FILE) as f:
    input_phrase = f.read()


pattern = r'mul\((\d{1,3}),(\d{1,3})\)'

muls = re.findall(pattern, input_phrase)

ans = sum([int(m[0]) * int(m[1]) for m in muls])

print(f"Part 1: {ans}")


pattern = r"mul\((\d{1,3}),(\d{1,3})\)|(do\(\)|don't\(\))"

muls = re.findall(pattern, input_phrase)

enabled = True
ans = 0
for m in muls:
    if m[2] == "do()":
        enabled = True
    elif m[2] == "don't()":
        enabled = False
    else:
        if enabled:
            ans += int(m[0]) * int(m[1])

print(f"Part 2: {ans}")
