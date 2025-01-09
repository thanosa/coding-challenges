'''

https://www.codingame.com/ide/puzzle/detective-pikaptcha-ep1

'''


def calc_nei(pos: tuple):
    up = (pos[0] - 1, pos[1])
    down = (pos[0] + 1, pos[1])
    left = (pos[0], pos[1] - 1)
    right = (pos[0], pos[1] + 1)
    return [up, down, left, right]


wall = []
space = []
width, height = [int(i) for i in input().split()]
for i in range(height):
    line = input()
    for j, c in enumerate(line):
        if c == "#":
            wall.append((j, i))
        else:
            space.append((j, i))

adj = {}      
for s in space:
    nei = calc_nei(s)
    a = 0
    for n in nei:
        if n is not s and n in space:
            a += 1
    adj[s] = a

for j in range(height):
    line = []
    for i in range(width):
        if (i, j) in wall:
            line.append("#")
        elif (i, j) in space:
            line.append(str(adj[(i, j)]))
        
    print(''.join(line))
