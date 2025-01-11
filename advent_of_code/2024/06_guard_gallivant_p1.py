INPUT_FILE = __file__.replace('_p1.py', '.py').replace('_p2.py', '.py').replace('.py', '.dat')

with open(INPUT_FILE) as f:
    world = f.read().strip().split('\n')

def read_position(char, world):
    for i, line in enumerate(world):
        for j, c in enumerate(line):
            if c == char:
                return (i, j)

def rotate_right(direction):
    return (direction % 4) + 1

def has_obstacle(direction: int, position: int, world: list[str]) -> bool:
    dx, dy = dd[direction]
    x, y = position
    return world[x + dx][y + dy] == "#"

def move_forward(direction: int, dd: dict[int, tuple[int, int]], position: tuple[int, int]) -> tuple[int, int]:
    dx, dy = dd[direction]
    x, y = position
    position = (x + dx, y + dy)
    return position

def is_move_out_of_bounds(position: int, world) -> bool:
    return position[0] < 0 or position[0] >= len(world) or position[1] < 0 or position[1] >= len(world[0])

dd = {
    1: (-1, 0),
    2: (0, 1),
    3: (1, 0),
    4: (0, -1)
}


direction = 1
position = read_position("^", world)
visited = set()

finished = False
while not finished:
    if has_obstacle(direction, position, world):
        direction = rotate_right(direction)

    position = move_forward(direction, dd, position)

    if is_move_out_of_bounds(position, world):
        finished = True
    visited.add(position)

print(f"{len(visited)}")
