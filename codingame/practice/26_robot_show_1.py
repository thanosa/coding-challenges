'''

https://www.codingame.com/training/easy/robot-show

'''


duct_length = int(input())
n = int(input())

positions = []
for i in input().split():
    positions.append(int(i))

print(max(duct_length - min(positions), max(positions)))
