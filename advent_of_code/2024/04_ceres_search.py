
INPUT_FILE=__file__.replace('.py', '.dat')

with open(INPUT_FILE) as f:
    lines = f.read().strip().split('\n')

n = len(lines)
m = len(lines[0])

dd = []
for dx in range(-1, 2):
    for dy in range(-1, 2):
        if dx != 0 or dy != 0:
            dd.append((dx, dy))

def has_xmas(i, j, d):
    dx, dy = d
    for k, x in enumerate("XMAS"):
        ii = i + k * dx
        jj = j + k * dy
        if not (0 <= ii < n and 0 <= jj < m):
            return False
        if lines[ii][jj] != x:
            return False
    return True

ans = 0
for i in range(n):
    for j in range(m):
        for d in dd:
            ans += has_xmas(i, j, d)

print(f"Part 1: {ans}")

dd = [
    (-1, -1),
    (-1, 1),
    (1, -1),
    (1, 1)
]

ans = 0
for i in range(1, n-1):
    for j in range(1, m-1):
        if lines[i][j] == "A":
            neighbors = []
            for d in dd:
                ii, jj = d
                neighbors.append(lines[i + ii][j + jj])

            if neighbors.count('M') == neighbors.count('S') == 2:
                if neighbors[0] != neighbors[3]:
                    ans += 1
        
print(f"Part 2: {ans}")
