from tqdm import tqdm

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

dd = {
    0: (-1, 0),  # Up
    1: (0, 1),   # Right
    2: (1, 0),   # Down
    3: (0, -1)   # Left
}

# Get the initial guard position
original_position = read_position("^", world)
creates_loop = 0

# Iterate through each cell to check for possible obstruction placements
for i in tqdm(range(len(world))):
    for j in range(len(world[0])):
        if (i, j) == original_position:
            continue
        
        # Modify the world temporarily by placing an obstruction
        new_world = [list(line) for line in world]  # Convert to list of lists for mutability
        new_world[i][j] = "#"
        new_world = ["".join(line) for line in new_world]  # Convert back to list of strings
        
        direction = 0  # Initial direction (Up)
        position = original_position
        visited = set()
        loop_detected = set()  # Track visited cycles with direction
        finished = False
        
        while not finished:
            # Print out the current position and direction for debugging
            print(f"Visiting position {position} with direction {direction}")

            if has_obstacle(direction, position, new_world):
                direction = rotate_right(direction)  # Turn right if obstacle encountered
            
            next_position = move_forward(direction, dd, position, new_world)

            if next_position is None:
                finished = True  # Out of bounds, stop the simulation
            elif (next_position, direction) in visited:
                # Avoid redundant loop detections if cycle is already marked
                if (next_position, direction) not in loop_detected:
                    loop_detected.add((next_position, direction))
                    print(f"Loop detected at {next_position} with direction {direction}")
                    creates_loop += 1  # Loop detected
                finished = True
            else:
                visited.add((next_position, direction))  # Mark position and direction as visited
                position = next_position
        exit()

print(f"Total loops created: {creates_loop}")
