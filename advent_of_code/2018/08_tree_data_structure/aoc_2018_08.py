import fileinput
import time
import re

INPUT_FILE = "aoc_2018_08.dat"

start = time.time()

inputs = list(map(int, [re.findall(r'\d+', x) for x in list(fileinput.input(INPUT_FILE))][0]))


class Node(object):
    def __init__(self, _inputs):
        self.inputs = _inputs
        self.children_miss = self.read_next()
        self.meta_count = self.read_next()
        self.meta_sum = 0
        self.child = None

        while self.children_miss > 0:
            self.children_miss -= 1
            self.child = Node(inputs)

            if self.child is not None:
                self.meta_sum += self.child.meta_sum
                self.child = None

        for _ in range(self.meta_count):
            self.meta_sum += self.read_next()

    def read_next(self):
        return self.inputs.pop(0)


result = Node(inputs).meta_sum

print("Part1: The result is: ", result)


print("Part2: The result is: ", result)
print("Seconds spent: ", round(time.time() - start, 5))
