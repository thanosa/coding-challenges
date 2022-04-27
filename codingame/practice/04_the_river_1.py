'''

https://www.codingame.com/training/easy/the-river-i-

'''

def next_drop(d: int) -> int:
    s = 0
    for c in str(d):
        s += int(c)
    return d + s
    
r1 = int(input())
r2 = int(input())

while r1 != r2:
    if r1 < r2:
        r1 = next_drop(r1)
    elif r2 < r1:
        r2 = next_drop(r2)
print(r1)
