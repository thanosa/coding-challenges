'''

https://www.codingame.com/ide/puzzle/abcdefghijklmnopqrstuvwxyz

'''

import sys

def debug(message):
    print(message, file=sys.stderr, flush=True)


class World:
    def __init__(self, text):
        self.text = text
        self.n = len(text)
    
    def get_neighbors(self, row, col):
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row = row + dx
            new_col = col + dy
            if 0 <= new_row < self.n and 0 <= new_col < self.n:
                neighbors.append((self.text[new_row][new_col], new_row, new_col))
        return neighbors
    
    def print(self, solution):
        for row in range(self.n):
            line = ""
            for col in range(self.n):
                line += chr(self.text[row][col]) if (row, col) in solution else '-'
            print(line)


class Searcher:
    def __init__(self, world):
        self.world = world
    
    def solve(self):
        for row in range(self.world.n):
            for col in range(self.world.n):
                path = self.search(ord('a'), row, col, [])
                if len(path) == 26:
                    return path[::-1]
        return []
    
    def search(self, search_idx, row, col, path):
        if self.world.text[row][col] != search_idx:
            return []
        
        path.append((row, col))
        
        if search_idx == ord('z'):
            return path
        
        for neighbor in self.world.get_neighbors(row, col):
            new_search_idx, new_row, new_col = neighbor
            if new_search_idx == search_idx + 1:
                path = self.search(new_search_idx, new_row, new_col, path)
        
        return path


n = int(input())
text = [list(map(ord, input())) for _ in range(n)]

world = World(text)
searcher = Searcher(world)
solution = searcher.solve()
world.print(solution)
