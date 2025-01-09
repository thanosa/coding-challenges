import time
import fileinput

INPUT_FILE = "aoc_2018_15.dat"


class Unit:
    def __init__(self, type_: str, pos: tuple):
        self.type = type_
        self.pos = pos
        self.hp = 300
        self.spaces = []

    def find_adj(self, spaces):
        neighbors = calc_neighbors(self.pos)
        self.spaces = [n for n in neighbors if n in spaces]

    def harm(self, damage=3) -> bool:
        self.hp -= damage
        return self.hp > 0


class Target:
    def __init__(self, unit: Unit):
        self.unit = unit
        self.ranged = None
        self.reachable = None
        self.dist = None
        self.nearest = None
        self.order = None


def calc_neighbors(pos: tuple) -> []:
    up = (pos.pos[0] - 1, pos.pos[1])
    down = (pos.pos[0] + 1, pos.pos[1])
    left = (pos.pos[0], pos.pos[1] - 1)
    right = (pos.pos[0], pos.pos[1] + 1)
    return [up, down, left, right]


def manhattan(pos1: tuple, pos2: tuple):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def read_board(input_file):
    units = []
    walls = []
    spaces = []

    board = list(fileinput.input(input_file))
    for y, line in enumerate(board):
        for x, char in enumerate(line):
            pos = (y, x)
            if char == 'E' or char == 'G':
                # Not sure if Elfs and Goblins should be in the same pool
                units.append(Unit(char, pos))
            elif char == '#':
                walls.append(pos)
            elif char == '.':
                spaces.append(pos)

    return units, walls, spaces


def game_ends(units):
    return len(units) <= 0


def sort_units(units):
    units.sort(key=lambda _x: _x.pos)


def calc_unit_spaces(units, spaces):
    for u in units:
        u.find_adj(spaces)


def calc_rooms(units, walls, spaces):
    rooms = 0
    for i, s in enumerate(spaces):
        pass

    return []


def __main__():

    start = time.time()
    units, walls, spaces = read_board(INPUT_FILE)

    while not (game_ends(units)):

        rooms = calc_rooms(units, walls, spaces)

        sort_units(units)
        calc_unit_spaces(units, spaces)

        for u in units:
            targets = [Target(t) for t in units if t is not u and t.type != u.type]
            ranged = set(s for t in targets for s in t.unit.spaces)

    print("Seconds spent: ", round(time.time() - start, 5))


__main__

















