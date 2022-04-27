'''

https://www.codingame.com/training/easy/rock-paper-scissors-lizard-spock

'''


import sys


def debug(message):
    print(message, file=sys.stderr, flush=True)


# Map of each symbol to which it wins
WINS = {
    'C': ['P', 'L'],
    'P': ['R', 'S'],
    'R': ['L', 'C'],
    'L': ['S', 'P'],
    'S': ['C', 'R'],
}


class Player():
    def __init__(self, number: int, sign: str):
        self.number = number
        self.sign = sign
        self.won = []
        self.alive = True

    def __repr__(self):
        return f"{self.number}"

    def fight(self, opponent):
        my_loosers = WINS[self.sign]

        # Tiebraker
        if opponent.sign == self.sign:
            if opponent.number < self.number:
                self.alive = False
                opponent.won.append(self)
            else:
                opponent.alive = False
                self.won.append(opponent)
        # We will
        elif opponent.sign in my_loosers:
            opponent.alive = False
            self.won.append(opponent)
        
        # We lose
        else:
            self.alive = False
            opponent.won.append(self)


# Ready meta
n = int(input())

players = []
for i in range(n):
    inputs = input().split()
    
    # Create a list of players
    players.append(
        Player(
            number=int(inputs[0]), 
            sign=inputs[1]
        ) 
    )

# Loop two players at a time:
while True:

    # Keep the active players onlt
    alive_players = [p for p in players if p.alive]

    # If we end up with 1 player then the tournament is over
    if len(alive_players) == 1:
        winner = [p for p in players if p.alive][0]
        print(f"{winner.number}")
        print(f"{' '.join(map(str, winner.won))}")
        exit(0)

    # Loop the players two by two
    for p1, p2 in zip(*[iter(alive_players)]*2):
        p1.fight(p2)
