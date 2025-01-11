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
    return (direction % 4) + 1

def has_obstacle(direction: int, position: tuple[int, int], world: list[str]) -> bool:
    dx, dy = dd[direction]
    x, y = position
    nx, ny = x + dx, y + dy
    if nx < 0 or nx >= len(world) or ny < 0 or ny >= len(world[0]):
        return False
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

def replace_in_world(world, i, j, replacement):
    if i < 0 or i >= len(world):
        raise ValueError("Line index out of range")
    if j < 0 or j >= len(world[i]):
        raise ValueError("Character index out of range")

    new_world = [line for line in world]
    line = list(new_world[i])
    line[j] = replacement
    new_world[i] = ''.join(line)
    return new_world

dd = {
    1: (-1, 0),
    2: (0, 1),
    3: (1, 0),
    4: (0, -1)
}

original_position = read_position("^", world)
creates_loop = 0

for i in range(len(world)):
    print("Checking row", i)
    for j in range(len(world[0])):
        direction = 1
        position = original_position

        if position == (i, j):
            continue
        world_temp = copy.deepcopy(world)
        new_world = replace_in_world(world_temp, i, j, "#")

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
