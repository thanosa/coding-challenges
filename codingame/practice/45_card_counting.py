'''

https://www.codingame.com/ide/puzzle/card-counting-when-easily-distracted

'''

import sys
from dataclasses import dataclass


def debug(message):
    print(message, file=sys.stderr, flush=True)


@dataclass
class Deck:
    cards: dict[str, tuple[int, int]]
    symbols: list[str]

    def __init__(self):
        self.symbols = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
        self.values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
        self.cards = {s: (v, 4) for s, v in zip(self.symbols, self.values)}

    def draw(self, symbol: str) -> None:
        value, remaining = self.cards[symbol]
        self.cards[symbol] = (value, remaining - 1)


stream = input()
bust = int(input())

# Initialize the deck
deck = Deck()

# Remove the cards from the deck if the chunk is valid
for s in stream.split('.'):
    if all([c in deck.symbols for c in s]):
        for c in s:
            deck.draw(c)

# Count the cards that do not bust and the total
total, safe = 0, 0
for _, (value, count) in deck.cards.items():
    total += count
    if value < bust:
        safe += count

# Print out the rounded percentage
print(f"{round(safe / total * 100)}%")
