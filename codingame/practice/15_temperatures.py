'''

https://www.codingame.com/training/easy/temperatures

'''


n = int(input())
b = 999999999

for i in input().split():
    t = int(i)
    if abs(t) < abs(b):
        b = t
    elif abs(t) == abs(b):
        b = max(t, b)

if b == 999999999:
    b = 0

print(b)
