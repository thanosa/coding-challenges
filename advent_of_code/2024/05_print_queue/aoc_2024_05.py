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


# reset the updates
updates = [line.split(",") for line in input_lines[separator_index + 1:]]

erroneous = []
for rule in rules:
    for update in updates[:]:  
        if not follows(update, rule):
            erroneous.append(update)

def swap_elements(lst, index1, index2):
    lst[index1], lst[index2] = lst[index2], lst[index1]



for update in erroneous:
    finished = False
    while not finished:
        for rule in rules:
            if not follows(update, rule):
                idx1 = update.index(rule[0])
                idx2 = update.index(rule[1])
                swap_elements(update, idx1, idx2)
                print(f"Not following rule: {rule} Swapped: {update})")
        
        for rule in rules:
            if not follows(update, rule):
                print(f"Update {update} still does not follow the rule {rule}.")
                finished = False
                break
        else:
            # print(f"Update follows all rules. {update}")
            finished = True

ans = 0

for update in erroneous:
    for rule in rules:
        if not follows(update, rule):
            print(f"Update {update} still does not follow the rule {rule}.")
    else:
        print(f"Update is ok: {update}")

    print(f"Middle element: {update[len(update) // 2]}")
    ans += int(update[len(update) // 2])

print(f"Part 2: {ans}")
