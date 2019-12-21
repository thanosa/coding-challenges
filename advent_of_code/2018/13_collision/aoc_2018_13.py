import time
import fileinput
from enum import Enum


INPUT_FILE = "aoc_2018_13.dat"
start = time.time()


class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class Choice(Enum):
    LEFT = 1
    STRAIGHT = 2
    RIGHT = 3


class Road(Enum):
    HORIZONTAL = "-"
    VERTICAL = "|"
    CROSS = "+"
    BACK_DIAG = "\\"
    FORWARD_DIAG = "/"


class Car:
    def __init__(self, _x: int, _y: int, _direction: Direction):
        self.x = _x
        self.y = _y
        self.direction = _direction
        self.choice = Choice.LEFT

    def move(self, _road: Road):
        if _road == Road.HORIZONTAL.value or _road == Road.VERTICAL.value:
            pass
        elif _road == Road.BACK_DIAG.value:
            if self.direction == Direction.RIGHT:
                self.direction = Direction.DOWN
            elif self.direction == Direction.DOWN:
                self.direction = Direction.RIGHT
            elif self.direction == Direction.LEFT:
                self.direction = Direction.UP
            elif self.direction == Direction.UP:
                self.direction = Direction.LEFT
        elif _road == Road.FORWARD_DIAG.value:
            if self.direction == Direction.LEFT:
                self.direction = Direction.DOWN
            elif self.direction == Direction.DOWN:
                self.direction = Direction.LEFT
            elif self.direction == Direction.RIGHT:
                self.direction = Direction.UP
            elif self.direction == Direction.UP:
                self.direction = Direction.RIGHT
        elif _road == Road.CROSS.value:
            if self.choice == Choice.LEFT:
                if self.direction == Direction.UP:
                    self.direction = Direction.LEFT
                elif self.direction == Direction.LEFT:
                    self.direction = Direction.DOWN
                elif self.direction == Direction.DOWN:
                    self.direction = Direction.RIGHT
                elif self.direction == Direction.RIGHT:
                    self.direction = Direction.UP
                self.choice = Choice.STRAIGHT
            elif self.choice == Choice.STRAIGHT:
                self.choice = Choice.RIGHT
            elif self.choice == Choice.RIGHT:
                if self.direction == Direction.UP:
                    self.direction = Direction.RIGHT
                elif self.direction == Direction.RIGHT:
                    self.direction = Direction.DOWN
                elif self.direction == Direction.DOWN:
                    self.direction = Direction.LEFT
                elif self.direction == Direction.LEFT:
                    self.direction = Direction.UP
                self.choice = Choice.LEFT

        if self.direction == Direction.RIGHT:
            self.x += 1
        elif self.direction == Direction.LEFT:
            self.x -= 1
        elif self.direction == Direction.DOWN:
            self.y += 1
        elif self.direction == Direction.UP:
            self.y -= 1


roads = list(fileinput.input(INPUT_FILE))
cars = []
for y, line in enumerate(roads):
    for x, character in enumerate(line):
        if character == ">":
            cars.append(Car(x, y, Direction.RIGHT))
        elif character == "<":
            cars.append(Car(x, y, Direction.LEFT))
        elif character == "^":
            cars.append(Car(x, y, Direction.UP))
        elif character == "v":
            cars.append(Car(x, y, Direction.DOWN))


for i, line in enumerate(roads):
    roads[i] = line.replace("<", "-").replace(">", "-").replace("^", "|").replace("v", "|")


def run_cars(_roads, _cars) -> int:
    turn = 0
    while True:
        turn += 1
        if len(cars) == 1:
            return cars[0].x, cars[0].y

        for car in sorted(cars, key=lambda c: (c.x, c.y)):
            road = roads[car.y][car.x]
            car.move(road)

            for other_car in cars:
                if other_car is not car:
                    if other_car.x == car.x and other_car.y == car.y:
                        print("Collision in turn: ", turn, car.x, car.y, other_car.x, other_car.y, len(cars))
                        cars.remove(car)
                        cars.remove(other_car)
                        break


collide_coordinates = run_cars(roads, cars)

print("Part1: The cars collided at: ", collide_coordinates)

print("Seconds spent: ", round(time.time() - start, 5))
