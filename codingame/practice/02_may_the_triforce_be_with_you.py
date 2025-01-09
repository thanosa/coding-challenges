'''

https://www.codingame.com/training/easy/may-the-triforce-be-with-you

'''

n = int(input())

width = (2 * n) - 1

# Construct the stared triangle as a building block
triangle = []
for i in range(n):
    spaces = ' ' * i
    stars = '*' * (width - (i * 2))
    line = spaces + stars + spaces
    # The lines are stored in a inverted order
    triangle.insert(0, line)

# build the upper part
for i in range(n):
    spaces = ' ' * n
    stars = triangle[i]
    line = spaces + stars
    
    # first character is a dot
    if i == 0:
        line = '.' + line[1:]
    print(line.rstrip())

# build the lower part
for i in range(n):
    spaces = ' '
    stars = triangle[i] 
    line = stars + spaces + stars
    print(line.rstrip())
