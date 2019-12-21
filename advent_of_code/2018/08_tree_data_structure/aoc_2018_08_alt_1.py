import fileinput
import time

INPUT_FILE = "aoc_2018_08.dat"

start = time.time()


def parse(it):
    num_children, num_metadata = next(it), next(it)
    children = [parse(it) for _ in range(num_children)]
    metadata = [next(it) for _ in range(num_metadata)]

    return metadata, children


def sum_metadata(node):
    metadata, children = node
    return sum(metadata) + sum(sum_metadata(x) for x in children)


def node_value(node):
    metadata, children = node
    if children:
        return sum(node_value(children[i - 1]) for i in metadata if 1 <= i <= len(children))
    return sum(metadata)


root = parse(map(int, next(fileinput.input(INPUT_FILE)).split()))

result = sum_metadata(root)
print("Part1: The result is: ", result)

result = node_value(root)
print("Part2: The result is: ", result)
print("Seconds spent: ", round(time.time() - start, 5))
