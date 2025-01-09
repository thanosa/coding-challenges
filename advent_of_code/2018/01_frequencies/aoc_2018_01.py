import fileinput
import time

INPUT_FILE = "aoc_2018_01.dat"

start = time.time()

inputs = list(map(int, list(fileinput.input(INPUT_FILE))))

my_sum = 0
seen = {my_sum}
isSolved = False
while not isSolved:
    for element in inputs:
        my_sum += element
        if my_sum not in seen:
            seen.add(my_sum)
        else:
            result = my_sum
            isSolved = True
            break

print("The result is: ", result)
print("Seconds spent: ", round(time.time() - start, 5))
