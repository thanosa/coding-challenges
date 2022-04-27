'''

https://www.codingame.com/training/easy/encryptiondecryption-of-enigma-machine

'''


import sys


def debug(message):
    print(message, file=sys.stderr, flush=True)

# Constant
LETTERS_COUNT = 26
CHARSET_SHIFT = 65

# Read input
operation = input()
shift = int(input())
rotors = []

# Read the rotors
for i in range(3):
    rotors.append(input())

# Encode
if operation == "ENCODE":
    # Read the message
    code = input()

    # Shift the letters based on a random number and an increment
    code = [chr(((ord(c) - CHARSET_SHIFT + shift + i) % LETTERS_COUNT) + CHARSET_SHIFT) for i, c in enumerate(code)]

    # Encode based on rotors
    for rotor in rotors:
        code = [rotor[(ord(c)-CHARSET_SHIFT) % LETTERS_COUNT] for c in code]
    
    # Output
    print(''.join(code))

# Decode
else:
    # Read the cipher
    code = input()

    # Decode based on rotors
    for rotor in reversed(rotors):
        code = [chr(CHARSET_SHIFT + rotor.index(c)) for c in code]
    
    # Shift back the letters based on a random number and an increment
    code = [chr(((ord(c) - CHARSET_SHIFT - shift - i) % LETTERS_COUNT) + CHARSET_SHIFT) for i, c in enumerate(code)]

    # Output
    print("".join(code))
