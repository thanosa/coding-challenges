'''

https://www.codingame.com/ide/puzzle/crop-circles

'''

import sys
from abc import abstractmethod


def debug(message):
    print(message, file=sys.stderr, flush=True)

CHAR_OFFSET = 96


class circle:
    x: int
    y: int
    radius: int

    def __init__(self, instruction):
        self.x = ord(instruction[0]) - CHAR_OFFSET
        self.y = ord(instruction[1]) - CHAR_OFFSET
        self.radius = int(instruction[2:])

    def __repr__(self):
        return f"{self.x},{self.y},{self.radius}"
    
    @abstractmethod
    def create(self):
        ...

    @classmethod
    def from_instruction(cls, instruction):
        if instruction.startswith("PLANTMOW"):
            return plantmow_circle.from_instruction(instruction[8:])
        elif instruction.startswith("PLANT"):
            return plant_circle.from_instruction(instruction[5:])
        else:
            return mow_circle.from_instruction(instruction)

class mow_circle(circle):
    def __init__(self, instruction):
        super().__init__(instruction)
    
    def create(self):
        print(f"mow circle {self.x},{self.y},{self.radius}")

class plant_circle(circle):
    def __init__(self, instruction):
        super().__init__(instruction)
    
    def create(self):
        print(f"plant circle {self.x},{self.y},{self.radius}")

class plantmow_circle(circle):
    def __init__(self, instruction):
        super().__init__(instruction)
    
    def create(self):
        print(f"plantmow circle {self.x},{self.y},{self.radius}")


height = 25
wide = 19
crop = '{}'
clear = '  '


instructions = input().split()
for instruction in instructions:
    debug(f"{instruction}")

    a = mow_circle(instruction)
    print(a)

    # if instruction.startswith("PLANTMOW"):
        