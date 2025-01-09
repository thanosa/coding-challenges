
INPUT_FILE=__file__.replace('.py', '.dat')

with open(INPUT_FILE) as f:
    input_lines = f.read().strip().split('\n')


def is_safe(values: list) -> bool:
    direction = None
    prev = None
    for cur in values:
        if prev is None:
            prev = cur
            continue
        
        diff = abs(cur - prev)

        if diff < 1 or diff > 3:
            return False

        if direction is None:
            direction = 'inc' if cur > prev else 'dec'
        
        if cur > prev and direction == 'dec' or cur < prev and direction == 'inc':
            return False
           
        prev = cur
    else:
        return True


safe = 0
for r in input_lines:
    values = [int(v) for v in r.split()]
    if is_safe(values): 
        safe += 1
   
print(f"Part 1: {safe}")


def generate_candidates(lst: list):
    yield lst
    for i in range(len(lst)):
        yield lst[:i] + lst[i+1:]

safe = 0
for r in input_lines:
    values = [int(v) for v in r.split()]

    for candidate in generate_candidates(values):
        if is_safe(candidate): 
            safe += 1
            break

print(f"Part 2: {safe}")
