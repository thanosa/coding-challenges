import sys
import math

from typing import Optional

def debug(msg):
    print(msg, file=sys.stderr, flush=True) 

def output_list(a_list):
    return ' '.join([x for x in a_list if x])

class App():
    def __init__(self, inputs_str):
        inputs = inputs_str.split()

        self.object_type = inputs[0]
        self._id = int(inputs[1])

        self.train = int(inputs[2])  # number of TRAINING skills needed to release this application
        self.code = int(inputs[3])  # number of CODING skills needed to release this application
        self.daily = int(inputs[4])  # number of DAILY_ROUTINE skills needed to release this application
        self.tasks = int(inputs[5])  # number of TASK_PRIORITIZATION skills needed to release this application
        self.arch = int(inputs[6])  # number of ARCHITECTURE_STUDY skills needed to release this application
        self.cd = int(inputs[7])  # number of CONTINUOUS_DELIVERY skills needed to release this application
        self.cr = int(inputs[8])  # number of CODE_REVIEW skills needed to release this application
        self.ref = int(inputs[9])  # number of REFACTORING skills needed to release this application

    def __repr__(self):
        card_types = [
            f"{self.train} train" if self.train else "",
            f"{self.code} code " if self.code else "",
            f"{self.daily} daily" if self.daily else "",
            f"{self.tasks} tasks" if self.tasks else "",
            f"{self.arch} arch " if self.arch else "",
            f"{self.cd} cd   " if self.cd else "",
            f"{self.cr} cr   " if self.cr else "",
            f"{self.ref} ref  " if self.ref else "",
        ]
        
        return f"{str(self._id).rjust(2, ' ')} {self.object_type} {output_list(card_types)}"

class Player():
    def __init__(self, inputs_str):
        # player_location: id of the zone in which the player is located
        # player_permanent_daily_routine_cards: number of DAILY_ROUTINE the player has played. It allows them to take cards from the adjacent zones
        # player_permanent_architecture_study_cards: number of ARCHITECTURE_STUDY the player has played. It allows them to draw more cards
        self.loc, self.score, self.daily, self.arch = [int(j) for j in inputs_str.split()]

        # Cards
        self.hand: Optional[Cards] = None
        self.auto: Optional[Cards] = None

    def __repr__(self):
        return f"at {self.loc}  score {self.score}  daily/arch {self.daily}/{self.arch}"

class Cards():
    def __init__(self, inputs_str):
        self.train = int(inputs_str[0])
        self.code = int(inputs_str[1])
        self.daily = int(inputs_str[2])
        self.tasks = int(inputs_str[3])
        self.arch = int(inputs_str[4])
        self.cd = int(inputs_str[5])
        self.cr = int(inputs_str[6])
        self.ref = int(inputs_str[7])
        self.bonus = int(inputs_str[8])
        self.debt = int(inputs_str[9])

    def __repr__(self):
        card_types = [
            f"{self.train} train" if self.train else "",
            f"{self.code} code " if self.code else "",
            f"{self.daily} daily" if self.daily else "",
            f"{self.tasks} tasks" if self.tasks else "",
            f"{self.arch} arch " if self.arch else "",
            f"{self.cd} cd   " if self.cd else "",
            f"{self.cr} cr   " if self.cr else "",
            f"{self.ref} ref  " if self.ref else "",
            f"{self.bonus} bonus" if self.bonus else "",
            f"{self.debt} debt " if self.debt else "",
        ]

        return f"{output_list(card_types)}"

# game loop
while True:
    # META
    game_phase = input()  # can be MOVE, GIVE_CARD, THROW_CARD, PLAY_CARD or RELEASE
    applications_count = int(input())
    debug(f"applications_count: {applications_count}")
    debug(f"game_phase: {game_phase}")
    
    # APPS
    apps = [App(input()) for _ in range(applications_count)]
    for app in apps:
        debug(f"{app}")

    # PLAYERS
    me = Player(input())
    foe = Player(input())
    debug(f" me: {me}")
    debug(f"foe: {foe}")

    # CARDS
    draw = discard = None
    card_locations_count = int(input())
    for i in range(card_locations_count):
        cards_input = input().split()
        location = cards_input[0]
        card_counts = cards_input[1:]
        cards = Cards(card_counts)

        if location == "HAND":
            me.hand = cards
        elif location == "AUTOMATED":
            me.auto = cards
        elif location == "OPPONENT_CARDS":
            foe.hand = cards
        elif location == "OPPONENT_AUTOMATED":
            foe.auto = cards
        elif location == "DRAW":
            draw = cards
        elif location == "DISCARD":
            discard = cards
        else:
            raise ValueError("Unexpected card location")
        
    debug(f" My cards: {me.hand} auto {me.auto}")
    debug(f"Foe cards: {foe.hand} auto {foe.auto}")
    debug(f"draw: {draw}")
    debug(f"discard: {discard}")


    possible_moves_count = int(input())
    for i in range(possible_moves_count):
        possible_move = input()


    # In the first league: RANDOM | MOVE <zoneId> | RELEASE <applicationId> | WAIT; In later leagues: | GIVE <cardType> | THROW <cardType> | TRAINING | CODING | DAILY_ROUTINE | TASK_PRIORITIZATION <cardTypeToThrow> <cardTypeToTake> | ARCHITECTURE_STUDY | CONTINUOUS_DELIVERY <cardTypeToAutomate> | CODE_REVIEW | REFACTORING;
    print("RANDOM")
