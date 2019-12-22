''' Advent of code 2019 Day 10 monitoring station'''

from collections import deque
from itertools import combinations
from math import atan2, degrees
from typing import NamedTuple


INPUT_FILE=__file__.replace('.py', '.dat')


class Asteroid(NamedTuple):
    x: int
    y: int


def calc_angle(a1: Asteroid, a2: Asteroid) -> float:

    changeInX = a2.x - a1.x
    changeInY = a2.y - a1.y

    angle = degrees(atan2(changeInY,changeInX))

    if angle < 0:
        angle += 360.0

    # rotate 90 degrees
    angle = (angle + 90) % 360

    return round(angle, 8)


def calc_manhattan(a1: Asteroid, a2: Asteroid):
    return abs(a1.x - a2.x) + abs(a1.y - a2.y)


def get_asteroids(input_map: str) -> list:
    # Converting the string into coordinates
    asteroids = []
    for y, line in enumerate(input_map.strip().split("\n")):
        for x, point in enumerate(line):
            if point == "#":
                asteroids.append(Asteroid(x, y))

    return asteroids

# For part 1
def find_station(asteroids: list) -> int:
    max_visibility = 0
    station = None
    angles = {}
    for a1 in asteroids:
        unique_angles = set()
        current_angles = {}
        for a2 in asteroids:
            dx = a1.x - a2.x
            dy = a1.y - a2.y
            if abs(dx) + abs(dy) > 0:
                angle = calc_angle(a1, a2)

                unique_angles.add(angle)

                distance = calc_manhattan(a1, a2)
                if angle not in current_angles:
                    current_angles[angle] = []
                current_angles[angle].append((a2, distance))

        cur_visibility = len(unique_angles)
        if cur_visibility > max_visibility:
            max_visibility = cur_visibility
            station = a1
            angles = current_angles

    # Sort the asteroids within each angle based on the distance.
    for k, v in angles.items():
	    angles[k] = sorted(v, key=lambda x: x[1])
    
    # Convert the dictionary to list, sorted by angle (key)
    sorted_angles = [deque(value) for (key, value) in sorted(angles.items(), reverse=False)]

    return max_visibility, station, sorted_angles


# For part 2
def vaporize_asteroids(station: Asteroid, angles: dict, vaporize_num=200) -> int:
    vaporize_count = 1
    pos = 0
    while len(angles) > 0:
        pos = pos % len(angles)
        asteroids = angles[pos]

        if len(asteroids) > 1:
            target = asteroids.popleft()[0]
            pos += 1
        else:
            target = asteroids[0][0]
            del angles[pos]

        if vaporize_count < vaporize_num:
            vaporize_count += 1
        else:
            return target


map_input = """
.#..#
.....
#####
....#
...##
"""
visibility, station, angles = find_station(get_asteroids(map_input))
assert visibility == 8 and station == Asteroid(3, 4)


map_input = """
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""
visibility, station, angles = find_station(get_asteroids(map_input))
assert visibility == 33 and station == Asteroid(5, 8)


map_input = """
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""
visibility, station, angles = find_station(get_asteroids(map_input))
assert visibility == 35 and station == Asteroid(1, 2)


map_input = """
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"""
visibility, station, angles = find_station(get_asteroids(map_input))
assert visibility == 41 and station == Asteroid(6, 3)


map_input = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""

# Part 2 asserts
tests = [
    [1, 11, 12   ],
    [2, 12, 1    ],
    [3, 12, 2    ],
    [10, 12, 8   ],
    [20, 16, 0   ],
    [50, 16, 9   ],
    [100, 10, 16 ],
    [199, 9, 6   ],
    [200, 8, 2   ],
    [201, 10, 9  ],
    [299, 11, 1  ],
]

for i, test in enumerate(tests):
    visibility, station, angles = find_station(get_asteroids(map_input))
    assert visibility == 210 and station == Asteroid(11, 13)

    target = vaporize_asteroids(station, angles, tests[i][0]) 
    assert target == Asteroid(tests[i][1], tests[i][2])

# Read the input
with open(INPUT_FILE) as f:
    input_string = f.read().strip()
    
# Part 1 solution
asteroids = get_asteroids(input_string)
visibility, station, angles = find_station(asteroids)
print(f"Part 1: {visibility}")

# Part 2 solution
final_asteroid = vaporize_asteroids(station, angles)
result2 = final_asteroid.x * 100 + final_asteroid.y
print(f"Part 2: {result2}")
