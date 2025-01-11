from tqdm import tqdm
import copy

INPUT_FILE = __file__.replace('_p1.py', '.py').replace('_p2.py', '.py').replace('.py', '.dat')

# Read the input
with open(INPUT_FILE) as f:
    world = f.read().strip().split('\n')


def read_position(char, world):
    for i, line in enumerate(world):
        for j, c in enumerate(line):
            if c == char:
                return (i, j)

def rotate_right(direction):
    return (direction + 1) % 4

def has_obstacle(direction: int, position: tuple[int, int], world: list[str]) -> bool:
    dx, dy = dd[direction]
    x, y = position
    nx, ny = x + dx, y + dy
    if nx < 0 or nx >= len(world) or ny < 0 or ny >= len(world[0]):
        return True  # Treat out-of-bounds as obstacles
    return world[nx][ny] == "#"

def move_forward(direction, dd, position, world):
    dx, dy = dd[direction]
    x, y = position
    nx, ny = x + dx, y + dy
    if nx < 0 or nx >= len(world) or ny < 0 or ny >= len(world[0]):
        return None  # Out of bounds
    return (nx, ny)

def is_move_out_of_bounds(position: int, world) -> bool:
    return position[0] < 0 or position[0] >= len(world) or position[1] < 0 or position[1] >= len(world[0])

dd = {
    0: (-1, 0),
    1: (0, 1),
    2: (1, 0),
    3: (0, -1)
}

original_position = read_position("^", world)
creates_loop = 0

for i in tqdm(range(len(world))):
    print("Checking row", i)
    for j in range(len(world[0])):
        if (i, j) == original_position:
            continue
        
        new_world = world[:]
        new_world[i] = new_world[i][:j] + "#" + new_world[i][j + 1:]

        direction = 0
        position = original_position

        visited = set()
        finished = False
        while not finished:
            if has_obstacle(direction, position, new_world):
                direction = rotate_right(direction)

            next_position = move_forward(direction, dd, position, new_world)
            if next_position is None:
                finished = True
            elif (next_position, direction) in visited:
                creates_loop += 1
                finished = True
            else:
                visited.add((next_position, direction))
                position = next_position 

print(creates_loop)
