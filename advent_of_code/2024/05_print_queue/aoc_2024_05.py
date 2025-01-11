INPUT_FILE = __file__.replace('.py', '.dat')

# Read the input
with open(INPUT_FILE) as f:
    input_lines = f.read().strip().split('\n')

# Parse input
separator_index = input_lines.index('')
rules = [line.split("|") for line in input_lines[:separator_index]]
updates = [line.split(",") for line in input_lines[separator_index + 1:]]

# Helper function to check if an update follows a rule
def follows(update, rule):
    if rule[0] in update and rule[1] in update:
        return update.index(rule[0]) < update.index(rule[1])
    return True

# Part 1: Identify valid updates and calculate sum of middle elements
valid_updates = []
for update in updates:
    if all(follows(update, rule) for rule in rules):
        valid_updates.append(update)

ans1 = sum(int(update[len(update) // 2]) for update in valid_updates)
print(f"Part 1: {ans1}")

# Part 2: Fix the erroneous updates
erroneous_updates = [update for update in updates if not all(follows(update, rule) for rule in rules)]

# Function to swap elements in a list
def swap_elements(lst, index1, index2):
    lst[index1], lst[index2] = lst[index2], lst[index1]

# Fix each erroneous update
for update in erroneous_updates:
    swap_made = True
    while swap_made:
        swap_made = False
        for rule in rules:
            if not follows(update, rule):
                idx1 = update.index(rule[0])
                idx2 = update.index(rule[1])
                swap_elements(update, idx1, idx2)
                swap_made = True

# Calculate the sum of middle elements for corrected updates
ans2 = sum(int(update[len(update) // 2]) for update in erroneous_updates)
print(f"Part 2: {ans2}")
