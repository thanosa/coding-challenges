'''

https://www.codingame.com/ide/puzzle/folding-paper

'''

import sys

def debug(message):
    print(message, file=sys.stderr, flush=True)


orders = input()
side = input()

relations = {
    "U": {
        "same": "U",
        "cross": "D",
        "near": ["L", "R"]
        },
    "D": {
        "same": "D",
        "cross": "U",
        "near": ["L", "R"],
    },
    "L": {
        "same": "L",
        "cross": "R",
        "near": ["U", "D"],
    },
    "R": {
        "same": "R",
        "cross": "L",
        "near": ["U", "D"],
    }
}


folds = {
    "U": 1,
    "D": 1,
    "L": 1,
    "R": 1,
}

for order in orders:
    new_folds = {
        "U": 0,
        "D": 0,
        "L": 0,
        "R": 0,
    }

    r = relations[order]
    
    new_folds = {
        r["same"]: 1,
        r["cross"]: folds[r["cross"]] + folds[r["same"]],
        r["near"][0]: folds[r["near"][0]] * 2,
        r["near"][1]: folds[r["near"][1]] * 2,
    }
    folds = new_folds

print(folds[side])
