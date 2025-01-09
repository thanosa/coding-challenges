'''

https://www.codingame.com/training/easy/1d-spreadsheet

'''


class Cell:
    def __init__(self, operation, arg_1, arg_2):
        self.operation = operation
        self.arg_1 = arg_1
        self.arg_2 = arg_2
        self.value = None

# Read input
n = int(input())
cells = []
for i in range(n):
    operation, arg_1, arg_2 = input().split()
    cells.append(Cell(operation, arg_1, arg_2))

# recursive function
def calc_cell(cells, i):
    c = cells[i]
    
    if c.value is not None:
        return int(c.value)
    
    if c.arg_1[0] == '$':
        c.arg_1 = calc_cell(cells, int(c.arg_1[1:]))
    
    if c.arg_2[0] == '$':
        c.arg_2 = calc_cell(cells, int(c.arg_2[1:]))
    
    if c.operation == 'VALUE':
        c.value = int(c.arg_1)
    elif c.operation == 'ADD':
        c.value = int(c.arg_1) + int(c.arg_2)
    elif c.operation == 'SUB':
        c.value = int(c.arg_1) - int(c.arg_2)
    elif c.operation == 'MULT':
        c.value = int(c.arg_1) * int(c.arg_2)
        
    return int(c.value)

# main
for i in range(n):
    calc_cell(cells, i)
        
# print output
for i in range(n):
    print(cells[i].value)
