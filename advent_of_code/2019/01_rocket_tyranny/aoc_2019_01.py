''' Advent of code 2019 Day 1: The Tyranny of the Rocket Equation'''

import math

INPUT_FILE=__file__.replace('.py', '.dat')

# For part 1
def calc_fuel(mass: int) -> int:
    return max(math.floor(mass / 3) - 2, 0)

# For part 2
def calc_recursive_fuel(mass: int) -> int:
    total = 0
    fuel = mass
    while True:
        fuel = calc_fuel(int(fuel))
        if fuel > 0:
            total += fuel    
        else:
            break
    return total

# Part 1 asserts
assert(calc_fuel(12) == 2)
assert(calc_fuel(14) == 2)
assert(calc_fuel(1969) == 654)
assert(calc_fuel(100756) == 33583)

# Part 1 solution
total = 0
for line in open(INPUT_FILE):
    total += calc_fuel(int(line))

print(f"Part 1: {total}")

# Part 2 asserts
assert(calc_recursive_fuel(14) == 2)
assert(calc_recursive_fuel(1969) == 966)
assert(calc_recursive_fuel(100756) == 50346)

# Part 2 solution
grand_total = 0
for mass in open(INPUT_FILE):
    grand_total += calc_recursive_fuel(mass)

print(f"Part 2: {grand_total}")
