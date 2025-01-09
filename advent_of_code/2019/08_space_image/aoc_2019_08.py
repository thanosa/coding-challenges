''' Advent of code 2019 Day 8: Space Image Format '''

import math
from typing import NamedTuple

INPUT_FILE=__file__.replace('.py', '.dat')

class Layer(NamedTuple):
    data: list
    meta: dict


def create_layers(data: str, width: int, height: int) -> list:
    layers = []
    pos = 0

    layer_count = math.floor(len(data) / (width * height))

    for l in range(layer_count):
        layer = []
        meta_dic = {}
        for i in range(height):
            row = []
            for j in range(width):
                pixel = data[pos]
                if pixel not in meta_dic:
                    meta_dic[pixel] = 1
                else:
                    meta_dic[pixel] += 1
                row.append(pixel)
                pos += 1
            layer.append(row)
        layers.append(Layer(data=layer, meta=meta_dic ))

    return layers

def validate(layers: list) -> int:
    min_zeros_layer = min(layers, key=lambda x: x.meta['0'])
    return min_zeros_layer.meta['1'] * min_zeros_layer.meta['2']

def print_message(layers: list, width: int, height: int):
    for h in range(height):
        row = []
        for w in range(width):
            for layer in layers:
                pixel = layer.data[h][w]
                if pixel != '2':
                    row.append(pixel)
                    break
        print("".join(row).replace("0", " ").replace("1", "#"))     
        

# Part 1 asserts
assert create_layers('123456789012', 3, 2)[0].data == [ ['1','2','3'], ['4','5','6'], ]
assert create_layers('123456789012', 3, 2)[1].data == [ ['7','8','9'], ['0','1','2'], ]
                               
# Read the input
with open(INPUT_FILE) as f:
    input_lines = f.read().strip()
    
# Part 1 solution
width = 25
height = 6 
layers = create_layers(input_lines, width, height)

result1 = validate(layers)
print(f"Part 1: {result1}")

# Part 2 solution
print(f"Part 2:")
print_message(layers, width, height)