'''

https://www.codingame.com/training/easy/detective-pikaptcha-ep1

'''


def rotate(d: int, side: str) -> int:
    if side == "R":
        return (d + 1) % 4
    else:
        return (d - 1) % 4

def calc_nei(pos: tuple, side: str, direction):
    up = (pos[0] - 1, pos[1])
    down = (pos[0] + 1, pos[1])
    left = (pos[0], pos[1] - 1)
    right = (pos[0], pos[1] + 1)
    
    if side == "R":
        if direction == 0:
            return [right, up, left, down]
        if direction == 1:
            return [down, right, up, left]
        if direction == 2:
            return [left, down, right, up]
        if direction == 3:
            return [up, left, down, right]
    else:
        if direction == 0:
            return [left, up, right, down]
        if direction == 1:
            return [up, right, down, left]
        if direction == 2:
            return [right, down, left, up]
        if direction == 3:
            return [down, left, up, right]

def calc_dir(pos, n):
    py = pos[0]
    px = pos[1]
    ny = n[0]
    nx = n[1]

    
    if ny == py:
        if nx < px:
            res = 3
        else:
            res = 1
    else:
        if nx == px:
            if ny < py:
                res = 0
            else:
                res = 2
    
    return res
    

wall = []
space = []
width, height = [int(i) for i in input().split()]
for j in range(height):
    line = input()
    for i, c in enumerate(line):
        if c == "#":
            wall.append((j, i))
        elif c == "0":
            space.append((j, i))
        elif c in ['^']:
            d = 0
            pos = (j, i)
            space.append((j, i))
        elif c in ['>']:
            d = 1
            pos = (j, i)
            space.append((j, i))
        elif c in ['v']:
            d = 2
            pos = (j, i)
            space.append((j, i))
        elif c in ['<']:
            d = 3
            pos = (j, i)
            space.append((j, i))
            
side = input()

init = pos


counter = {}
stop = False
while stop == False:
    nei = calc_nei(pos, side, d)
    
    for cn, n in enumerate(nei):
        if n in space:
            d = calc_dir(pos, n)
            pos = n
           
            if n in counter:
                counter[n] += 1
            else:
                counter[n] = 1
            break
    
    if pos == init:
        stop = True


for i in range(height):
    line = []
    for j in range(width):
        if (i, j) in wall:
            line.append("#")
        elif (i, j) in space:
            if (i, j) in counter:
                r = counter[(i, j)]
            else:
                r = 0
            line.append(str(r))

    print(''.join(line))
