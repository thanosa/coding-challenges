'''

https://www.codingame.com/training/easy/object-insertion

'''


# Read data
a, b = [int(i) for i in input().split()]
obj = []
for i in range(a):
    object_line = [s for s in input()]
    obj.append(object_line)

c, d = [int(i) for i in input().split()]
grid = []
for i in range(c):
    grid_line = [s for s in input()]
    grid.append(grid_line)

# solution
matches = 0
for row in range(c - a + 1):
    for col in range(d - b + 1):
       
        does_not_fit = False
        for i in range(a):
            if does_not_fit:
                break
            for j in range(b):
                if obj[i][j] == '*' and grid[row + i][col + j] == '#':
                    does_not_fit = True
                    break
        
        if not does_not_fit:
            matches += 1
            last_solution_row = row
            last_solution_col = col

print(matches)

if matches == 1:
    for row in range(c):
        solution_row = []
        for col in range(d):
            grid_char = grid[row][col]

            is_within_solution_row = (row >= last_solution_row) and (row < last_solution_row + a)
            is_within_solution_col = (col >= last_solution_col) and (col < last_solution_col + b)

            if is_within_solution_row and is_within_solution_col:
                obj_char = obj[row - last_solution_row][col - last_solution_col]
                if obj_char == '*':
                    solution_char = '*'
                else:
                    solution_char = grid_char
            else:
                solution_char = grid_char
            solution_row.append(solution_char)

        print("".join(solution_row))
