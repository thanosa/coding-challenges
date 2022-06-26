'''

https://www.codingame.com/ide/puzzle/logic-gates

'''

import numpy as np
import sys

def debug(msg):
    print(msg, file=sys.stderr, flush=True) 


def calc(_type: str, input_1: np.ndarray, input_2: np.ndarray) -> str:
    
    result = []

    if _type == "AND":
        result = np.bitwise_and(input_1, input_2)
    elif _type == "OR":
        result = np.bitwise_or(input_1, input_2)
    elif _type == "XOR":
        result = np.bitwise_xor(input_1, input_2)
    elif _type == "NAND":
        result = np.invert(np.bitwise_and(input_1, input_2))
    elif _type == "NOR":
        result = np.invert(np.bitwise_or(input_1, input_2))
    elif _type == "NXOR":
        result = np.invert(np.bitwise_xor(input_1, input_2))

    return ''.join(['-' if x else '_' for x in result])


n = int(input())
m = int(input())
inputs = {}
for i in range(n):
    input_name, input_signal = input().split()
    inputs[input_name] = np.array([x == '-' for x in input_signal])

outputs = {}
for i in range(m):
    output_name, _type, input_name_1, input_name_2 = input().split()
    out = calc(_type, inputs[input_name_1], inputs[input_name_2])
    print(f"{output_name} {out}")
