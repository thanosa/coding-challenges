INPUT_FILE=__file__.replace('.py', '.dat')

# Read the input
with open(INPUT_FILE) as f:
    input_lines = f.read().strip().split('\n')
    

separator_index = input_lines.index('')
rules = [line.split("|") for line in input_lines[:separator_index]]
updates = [line.split(",") for line in input_lines[separator_index + 1:]]

def follows(update, rule):

    if rule[0] in update and rule[1] in update:
        return update.index(rule[0]) < update.index(rule[1])
    else:
        return True

for rule in rules:
    for update in updates[:]:  
        if not follows(update, rule):
            updates.remove(update)

ans = 0
for update in updates:
    ans += int(update[len(update) // 2])

print(f"Part 1: {ans}")

# print(f"Part 2: {0}")
