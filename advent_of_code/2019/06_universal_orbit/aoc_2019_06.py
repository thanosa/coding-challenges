''' Advent of code 2019 Day 6 - Universal Orbit Map'''
from collections import deque

INPUT_FILE=__file__.replace('.py', '.dat')

def count_subtree_orbits(parent, planetary) -> int:
    count = 0
    for child in planetary.get(parent, []):
        count += 1
        count += count_subtree_orbits(child, planetary)
        
    return count

def create_single_planetary(orbits: list) -> set:
    planetary = {}
    for orbit in orbits:
        planets = orbit.strip().split(')')
        
        if planets[0] not in planetary:
            planetary[planets[0]] = []
        planetary[planets[0]].append(planets[1])

    return planetary

def create_double_planetary(orbits: list) -> set:
    planetary = {}
    for orbit in orbits:
        planets = orbit.strip().split(')')
        
        if planets[0] not in planetary:
            planetary[planets[0]] = []
        planetary[planets[0]].append(planets[1])

        if planets[1] not in planetary:
            planetary[planets[1]] = []
        planetary[planets[1]].append(planets[0])

    return planetary

def count_orbits(orbits: list) -> int:
    planetary = create_single_planetary(orbits)

    count = 0
    for planet in planetary:
        count += count_subtree_orbits(planet, planetary)
    
    return count

def count_transfers(orbits: list, source: str = 'YOU', destination: str = 'SAN') -> int:
    planetary = create_double_planetary(orbits)
    distances = {}
    planets = deque()
    planets.append((source, 0))
    while planets:
        planet, distance = planets.popleft()
        if planet in distances:
            continue
        distances[planet] = distance
        for child in planetary[planet]:
            planets.append((child, distance + 1))
    
    return distances[destination] - 2


# Part 1 asserts
assert count_orbits(['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L']) == 42

# Part 1 solution
with open(INPUT_FILE) as f:
    input_list = f.read().strip().split('\n')
    result1 = count_orbits(input_list)

print(f"Part 1: {result1}")
assert result1 == 117672

# Part 2 asserts
assert count_transfers(['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L', 'K)YOU', 'I)SAN']) == 4

# Part 2 solution
result2 = count_transfers(input_list)
print(f"Part 2: {result2}")
