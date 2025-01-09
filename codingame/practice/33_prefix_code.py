'''

https://www.codingame.com/training/easy/prefix-code

'''


def find_unique_lengths(inputs: dict) -> set:
    """
    Given a dictionary, return a set of integers
    representing the unique lengths of the input strings
    """
    return set([len(str(s)) for s in inputs])


n = int(input())
tokens = {}
for i in range(n):
    inputs = input().split()
    b = inputs[0]
    c = int(inputs[1])
    tokens[b] = c

lengths = find_unique_lengths(tokens)

s = input()

i = 0
out = []
while True:
    if i == len(s):
        break

    for length in lengths:
        token = s[i:i+length]
        if token in tokens:
            out.append(tokens[token])
            i += len(token)
            break
    else:
        print(f"DECODE FAIL AT INDEX {i}")
        exit(0)

print("".join([chr(n) for n in out]))
