'''

https://www.codingame.com/training/easy/equivalent-resistance-circuit-building

'''


# Dictionary that stores the value of each resistance name 
ohms = {}

# Read the inputs
n = int(input())
for i in range(n):
    inputs = input().split()
    name = inputs[0]
    value = int(inputs[1])

    # Populate the ohms dictionary    
    ohms[name] = value

# Construct the circuit and replace the names with their resistance values
circuit = [ohms[e] if e in ohms else e for e in input().split()]

# Constants
OPENING_CHARACTERS = ['[', '(']
CLOSING_CHARACTERS = [']', ')']

while len(circuit) > 1:
    for i, e in enumerate(circuit):
        if e in OPENING_CHARACTERS:
            start = i
            resistances = []
            connection_is_serial = e == '('
            value = None
            
        elif e in CLOSING_CHARACTERS:
            end = i

            # Calculate the value depending on the circuite type
            if connection_is_serial:
                value = sum(resistances)
            else:
                value = 1 / (sum([(1 / r) for r in resistances]))
            break
        else:
            resistances.append(e)

    # Update the circuit replacing the branch with its value
    if value:
        circuit = circuit[:start] + [value] + circuit[end+1:]
    else:
        circuit = circuit[:start] + circuit[end+1:]

# Output
print(round(float(value), 1))
