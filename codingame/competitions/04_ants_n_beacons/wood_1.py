import math
import sys

from typing import List, Tuple, Optional


def debug(message):
    print(message, file=sys.stderr, flush=True)


class Cell(object):
    index: int
    cell_type: int # 0 for empty, 1 for eggs, 2 for crystal
    resources: int
    neighbors: list[int]
    my_ants: int
    opp_ants: int
    my_dist: Optional[int]
    opp_dist: Optional[int]

    def __init__(self, index: int, cell_type: int, resources: int, neighbors: list[int], my_ants: int, opp_ants: int):
        self.index = index
        self.cell_type = cell_type
        self.resources = resources
        self.neighbors = neighbors
        self.my_ants = my_ants
        self.opp_ants = opp_ants
        self.my_dist = None
        self.my_dist = None

    def __repr__(self):
        # return f"I:{self.index} T:{self.cell_type} R:{self.resources} A:{self.my_ants}/{self.opp_ants} "
        return f"{self.index}"
      

class World(object):
    cells: List[Cell]

    def __init__(self, cells: List[Cell], my_bases_idx: List[int], opp_bases_idx: List[int]) -> None:
        self.cells = cells
        self._my_bases_idx = my_bases_idx
        self._opp_bases_idx = opp_bases_idx

    @property
    def cells_count(self) -> int:
        return len(self.cells)

    @property
    def my_bases(self):
        return [self.cells[i] for i in self._my_bases_idx]

    @property
    def opp_bases(self):
        return [self.cells[i] for i in self._opp_bases_idx]


def read_cell_inputs() -> List[Cell]:
    cells: List[Cell] = []

    number_of_cells = int(input())  
    for i in range(number_of_cells):
        inputs = [int(j) for j in input().split()]

        cell: Cell = Cell(
            index = i,
            cell_type = inputs[0], 
            resources = inputs[1], 
            neighbors = list(filter(lambda direction: direction > -1, inputs[2:8])),
            my_ants = 0,
            opp_ants = 0
        )
        cells.append(cell)

    return cells


def read_bases() -> Tuple[List[int], List[int]]:

    _ = int(input()) # the number of bases are not needed
    my_bases: list[int] = [int(i) for i in input().split()]
    opp_bases: list[int] = [int(i) for i in input().split()]
    debug(f"MY_BASES:{my_bases}  OPP_BASES:{opp_bases}")

    return my_bases, opp_bases


def find_path(cell1: Cell, cell2: Cell) -> List[Cell]:
    # Keep track of the visited cells
    visited = set()

    # Keep track of the path
    path = {}
    path[cell1] = None

    # Perform BFS
    queue = [cell1]
    while queue:
        current_cell = queue.pop(0)
        visited.add(current_cell)

        if current_cell.index == cell2.index:
            # debug(f"check the queue: {[c.index for c in queue]}")
            # debug(f"check the path: {path}")
            # Reconstruct the path
            shortest_path = []
            while current_cell:
                shortest_path.append(current_cell)
                # debug(f"shortest: {shortest_path}")
                current_cell = path[current_cell]
            return shortest_path[::-1]

        # debug(f"current cell: {current_cell.index} with neighbors: {current_cell.neighbors}")
        for neighbor_index in current_cell.neighbors:
            neighbor_cell = world.cells[neighbor_index]
            if neighbor_cell not in visited:
                queue.append(neighbor_cell)
                visited.add(neighbor_cell)
                path[neighbor_cell] = current_cell
            # debug(f"PATH:{[(k.index, v) for k, v in path.items()]}")
    
    # If no path is found
    return []


def calc_min_distance(bases: List[Cell], cell: Cell) -> Tuple[int, Cell]:
    min_distance = 99999
    min_base: Cell = bases[0]

    for base in bases:
        path = find_path(base, cell)
        # debug(f"PATH: base{base.index} to {cell.index}: {[c.index for c in path]}")
        if len(path) < min_distance:
            min_distance = len(path)
            min_base = base
    return min_distance, min_base


def max_to_challenger(world: World) -> List:
    # Find the challenger cell and create a line on it
    
    min_abs_diff = 99999
    challenger: Optional[Cell] = world.cells[0]
    my_base = world.my_bases[0]

    for c in world.cells:
        if not c.resources > 0:
            continue
        # debug(f"Checking cell: {c.index}")

        c.my_dist, my_base = calc_min_distance(world.my_bases, c)
        c.opp_dist, _ = calc_min_distance(world.opp_bases, c)
        abs_diff = abs(c.my_dist - c.opp_dist)

        # debug(f"c.my_dist{c.my_dist}  c.opp_dist{c.opp_dist}  abs_diff{abs_diff}")
        if abs_diff < min_abs_diff:
            min_abs_diff = abs_diff
            challenger = c

    action = f"LINE {my_base.index} {challenger.index} 1"
    debug(action)
    return [action]


_cells = read_cell_inputs()
_my_bases_idx, _opp_bases_idx = read_bases()
world = World(
    cells=_cells,
    my_bases_idx=_my_bases_idx,
    opp_bases_idx=_opp_bases_idx,
)


# game loop
while True:
    for i in range(world.cells_count):
        c = world.cells[i]
        c.resources, c.my_ants, c.opp_ants = [int(j) for j in input().split()]

        c.my_dist, _ = calc_min_distance(world.my_bases, c)
        c.opp_dist, _ = calc_min_distance(world.opp_bases, c)

    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
    actions = max_to_challenger(world)

    if len(actions) == 0:
        print('WAIT')
    else:
        print(';'.join(actions))
