'''

https://www.codingame.com/ide/puzzle/crop-circles

'''

import sys

from typing import List


def debug(message):
    print(message, file=sys.stderr, flush=True)


class Settings:
    char_offset = 96


class Symbols:
    crop = '{}'
    empty = '  '


class World:
    height = 25
    length = 19


class Circle:
    x: float
    y: float
    diameter: float

    def __init__(self, instruction):
        self.x = ord(instruction[0]) - Settings.char_offset
        self.y = ord(instruction[1]) - Settings.char_offset
        self.diameter = float(instruction[2:])

    def pr(self):
        return f"circle {self.x},{self.y},{self.diameter}"


class MowCircle(Circle):
    def __init__(self, instruction):
        super().__init__(instruction)
    
    def __repr__(self):
        return f"mow {super().pr()}"


class PlantCircle(Circle):
    def __init__(self, instruction):
        super().__init__(instruction)
    
    def __repr__(self):
        return f"plant {super().pr()}"


class PlantMowCircle(Circle):
    def __init__(self, instruction):
        super().__init__(instruction)
    
    def __repr__(self):
        return f"plantmow {super().pr()}"


class CircleBuilder:
    @classmethod
    def build(cls, instruction):
        if instruction.startswith("PLANTMOW"):
            return PlantMowCircle(instruction[8:])
        elif instruction.startswith("PLANT"):
            return PlantCircle(instruction[5:])
        else:
            return MowCircle(instruction)


class Imprints:
    mows: List[MowCircle]
    plants: List[PlantCircle]
    plant_mows: List[PlantMowCircle]

    def __init__(self):
        self.mows = []
        self.plants = []
        self.plant_mows = []

    def add(self, circle: Circle):
        if isinstance(circle, MowCircle):
            self.mows.append(circle)
        elif isinstance(circle, PlantCircle):
            self.plants.append(circle)
        elif isinstance(circle, PlantMowCircle):
            self.plant_mows.append(circle)
        else:
            raise ValueError(f"Invalid circle instance: {type(circle)}")
    
    def _is_in_circle(self, x: float, y: float, circle: Circle) -> bool:
        distance = ((circle.x - x) ** 2 + (circle.y - y) ** 2) ** 0.5
        return distance <= (circle.diameter / 2)

    def is_in_mows(self, x: float, y: float) -> bool:
        return any([self._is_in_circle(x, y, circle) for circle in self.mows])

    def is_in_plants(self, x: float, y: float) -> bool:
        return any([self._is_in_circle(x, y, circle) for circle in self.plants])
    
    def is_in_plant_mows(self, x: float, y: float) -> bool:
        return sum([1 if self._is_in_circle(x, y, circle) else 0 for circle in self.plant_mows]) % 2 == 1


imprints = Imprints()

for instruction in input().split():
    circle = CircleBuilder.build(instruction)
    imprints.add(circle)

for y in range(1, World.height + 1):
    line = ""
    for x in range(1, World.length + 1):
        in_mows = imprints.is_in_mows(x, y)
        in_plants = imprints.is_in_plants(x, y)
        in_plant_mows = imprints.is_in_plant_mows(x, y)
        
        mow = (in_mows and not in_plants)
        if in_plant_mows:
            mow = not mow

        line += Symbols.empty if mow else Symbols.crop 
    print(line)
