'''

https://www.codingame.com/training/easy/ghost-legs

'''

w, h = [int(i) for i in input().split()]
m = []

for i in range(h):
    line = input()
    if i == 0:
        header = line.replace(' ', '')
    elif i == h - 1:
        footer = line.replace(' ', '')
    else:
        m.append(line.replace('  ', '').replace('|--|','><'))

w = len(header)
for col in range(w):
    curcol = col
    for line in m:
        me = line[curcol]
        if curcol > 0:
            left = line[curcol - 1]
        if curcol < w - 1:
            right = line[curcol + 1]
            
        if me == '<' and left == '>':
            curcol -= 1
        elif me == '>' and right == '<':
            curcol += 1

    print(header[col] + footer[curcol])
