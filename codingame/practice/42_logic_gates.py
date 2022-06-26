'''

https://www.codingame.com/training/easy/logic-gates

'''

import numpy as np

def calc(_type: str, input_1: np.ndarray, input_2: np.ndarray) -> np.ndarray:
    
    invert = _type[0] == 'N'
    operation = _type if not invert else _type[1:]

    f = {
        "AND": np.bitwise_and,
        "OR": np.bitwise_or,
        "XOR": np.bitwise_xor
    }

    result = f[operation](input_1, input_2)
    return result if not invert else np.invert(result)

n, m = int(input()), int(input())

inputs = {}
for i in range(n):
    input_name, input_signal = input().split()
    inputs[input_name] = np.array([x == '-' for x in input_signal])

for i in range(m):
    output_name, _type, input_name_1, input_name_2 = input().split()
    result = calc(_type, inputs[input_name_1], inputs[input_name_2])
    converted = ''.join(['-' if x else '_' for x in result])
    print(f"{output_name} {converted}")
