import time

INPUT_FILE = "aoc_2018_09.dat"


class Game:
    def __init__(self, _players_cnt, _last_marble):
        self.players_count = _players_cnt
        self.last_marble = _last_marble
        self.score = [0] * _players_cnt
        self.player = -1
        self.marble = -1

    def next_player(self):
        if self.marble == self.last_marble + 1:
            print("Part1: The result is: ", max(self.score))
            exit(0)
        else:
            self.marble += 1
            self.player += 1
            if divmod(int(self.player), self.players_count)[1] == 0:
                self.player = 0

    def add_score(self, _value):
        self.score[self.player] += _value


class Circle:
    def __init__(self):
        self.marbles = []
        self.cur_marble = -1

    def use(self, _marble) -> int:
        if _marble != 0 and divmod(_marble, 23)[1] == 0:
            return self.remove_marble(_marble)
        else:
            self.add_marble(_marble)
            return 0

    def add_marble(self, _marble):
        # When there is no marble or only 1 marble
        if len(self.marbles) in [0, 1]:
            self.marbles.append(_marble)
            self.cur_marble = len(self.marbles) - 1

        # When the current marble is the last
        elif self.cur_marble == len(self.marbles) - 1:
            self.marbles.insert(1, _marble)
            self.cur_marble = 1

        # When the current marble is second from last
        elif self.cur_marble == len(self.marbles) - 2:
            self.marbles.append(_marble)
            self.cur_marble = len(self.marbles) - 1

        # Any other case
        else:
            self.marbles.insert(self.cur_marble + 2, _marble)
            self.cur_marble += 2

    def remove_marble(self, _marble) -> int:
        remove_marble = self.marbles[self.cur_marble - 7]
        self.marbles.pop(self.cur_marble - 7)
        self.cur_marble = (self.cur_marble - 7) % len(self.marbles)
        return _marble + remove_marble

    def print_circle(self):
        res = ""
        for i, marble in enumerate(self.marbles):
            if i == self.cur_marble:
                out = "(" + str(marble) + ")"
            else:
                out = str(marble)
            res = res + " " + out
        print(res)

start = time.time()

players_cnt, last_marble = 13, 7999  # 146071 instead of 146373
players_cnt, last_marble = 17, 1104  # ok 2764
players_cnt, last_marble = 21, 6111  # ok 54718
players_cnt, last_marble = 30, 5807  # ok 37305
players_cnt, last_marble = 10, 1618  # ok 8317
players_cnt, last_marble = 452, 71250  # 384317 instead of 398730

game = Game(players_cnt, last_marble)
circle = Circle()
while True:
    game.next_player()
    game.add_score(circle.use(game.marble))
    # circle.print_circle()


result = 0
print("Part2: The result is: ", result)
print("Seconds spent: ", round(time.time() - start, 5))
