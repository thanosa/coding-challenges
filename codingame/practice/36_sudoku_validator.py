'''

https://www.codingame.com/ide/puzzle/sudoku-validator

'''


def verify_list(lst):
    if len(set(lst)) != 9:
        print("false")
        exit(0)


game = []
for i in range(9):
    game.append(list(map(int, input().split())))
    
# Check rows
for row in game:
    verify_list(row)
    
# Check columns
for c in range(9):
    col = [row[c] for row in game]
    verify_list(col)

# Check subgrid
for xs in range(3):
    for ys in range(3):
        sub = []
        for xc in range(3):
            for yc in range(3):
                x, y = (3 * xs) + xc, (3 * ys) + yc
                sub.append(game[y][x])
        verify_list(sub)

print("true")
