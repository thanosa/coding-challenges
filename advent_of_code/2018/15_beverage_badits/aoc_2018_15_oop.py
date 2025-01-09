import time
import fileinput

INPUT_FILE = "aoc_2018_15.dat"


def manhattan(pos1: tuple, pos2: tuple):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


class Unit:
    def __init__(self, _unit_type: str, _pos: tuple):
        self.unit_type = _unit_type
        self.pos = _pos
        self.hp = 300

    def harm(self, damage=3) -> bool:
        self.hp -= damage
        return self.hp > 0

    def move(self):
        pass

    def attack(self):
        pass


class Board:
    def __init__(self, init_state):
        self.units = []
        self.wall = []
        self.space = []
        for y, line in enumerate(init_state):
            for x, char in enumerate(line):
                pos = (y, x)
                # Not sure if I should  keep all units in the same array
                if char == 'E' or char == 'G':
                    self.units.append(Unit(char, pos))
                elif char == '#':
                    self.wall.append(pos)
                elif char == '.':
                    self.space.append(pos)

    def game_ends(self) -> bool:
        return len(self.units) <= 0

    def sort_units(self):
        self.units.sort(key=lambda x: x.pos)


start = time.time()
INPUT_FILE = 'aoc_2018_15.dat'
input_board = list(fileinput.input(INPUT_FILE))

b = Board(input_board)
while not(b.game_ends()):
    b.sort_units()
    for u in b.units:
        u.move()
        u.attack()


print("Seconds spent: ", round(time.time() - start, 5))

