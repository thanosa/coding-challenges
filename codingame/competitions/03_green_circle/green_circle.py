import sys
from typing import Optional


def debug(msg):
    print(msg, file=sys.stderr, flush=True) 


def output_list(a_list):
    return '  '.join([str(x) for x in a_list if x])


class App():
    def __init__(self, inputs_str):
        inputs = inputs_str.split()

        self.object_type = inputs[0]
        assert self.object_type == "APPLICATION"

        self._id = int(inputs[1])

        self.train = int(inputs[2])  # number of TRAINING skills needed to release this application
        self.code = int(inputs[3])  # number of CODING skills needed to release this application
        self.daily = int(inputs[4])  # number of DAILY_ROUTINE skills needed to release this application
        self.tasks = int(inputs[5])  # number of TASK_PRIORITIZATION skills needed to release this application
        self.arch = int(inputs[6])  # number of ARCHITECTURE_STUDY skills needed to release this application
        self.cd = int(inputs[7])  # number of CONTINUOUS_DELIVERY skills needed to release this application
        self.cr = int(inputs[8])  # number of CODE_REVIEW skills needed to release this application
        self.ref = int(inputs[9])  # number of REFACTORING skills needed to release this application
        self.specs = [
            self.train,
            self.code,
            self.daily,
            self.tasks,
            self.arch,
            self.cd,
            self.cr,
            self.ref,
        ]

    def __repr__(self):
        return f"{str(self._id).rjust(2, ' ')} {self.specs}"


class Player():
    def __init__(self, inputs_str):
        # player_location: id of the zone in which the player is located
        # player_permanent_daily_routine_cards: number of DAILY_ROUTINE the player has played. It allows them to take cards from the adjacent zones
        # player_permanent_architecture_study_cards: number of ARCHITECTURE_STUDY the player has played. It allows them to draw more cards
        self.loc, self.score, self.daily, self.arch = [int(j) for j in inputs_str.split()]

        # Cards for me
        self.hand: Optional[Cards] = None
        self.draw: Optional[Cards] = None
        self.discard: Optional[Cards] = None

        # Cards for me and foe
        self.auto: Optional[Cards] = None

        # Cards for foe
        self.cards: Optional[Cards] = None

    def __repr__(self):
        return f"at {self.loc}  score {self.score}  daily {self.daily}  arch {self.arch}"


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


def print_info(phase, actions, apps, me, foe):
    app_header = "   [0, 1, 2, 3, 4, 5, 6, 7]"

    debug(f"PHASE: {phase}")
    debug(f"ACTIONS: {output_list(actions)}")
    debug("")
    debug(app_header)
    for app in apps:
        debug(f"{app}")
    debug(app_header)
    debug("")
    debug(f"ME: {me}")
    debug(f"HAND: {me.hand}")
    debug(f"DRAW: {me.draw}")
    debug(f"DISC: {me.discard}")
    debug(f"AUTO: {me.auto}")
    debug("")
    debug(f"  FOE: {foe}")
    debug(f"CARDS: {foe.cards}")
    debug(f" AUTO: {foe.auto}")


def calc_deficit(apps, my_hand):
    """
    Calculate the deficit of the cards for each of the application
    """

    pass


def play(phase, actions, apps, me, foe):
    # In the first league: RANDOM | MOVE <zoneId> | RELEASE <applicationId> | WAIT
    #
    # In later leagues: | GIVE <cardType> | THROW <cardType> | TRAINING | CODING | DAILY_ROUTINE 
    #                   | TASK_PRIORITIZATION <cardTypeToThrow> <cardTypeToTake> | ARCHITECTURE_STUDY 
    #                   | CONTINUOUS_DELIVERY <cardTypeToAutomate> | CODE_REVIEW | REFACTORING

    # Check if there is immediately releasable software
    
    return "RANDOM"

# game loop
while True:
    # PHASE
    phase = input()  # can be MOVE, GIVE_CARD, THROW_CARD, PLAY_CARD or RELEASE
    
    # APPS
    apps = [App(input()) for _ in range(int(input()))]

    # PLAYERS
    me = Player(input())
    foe = Player(input())

    # CARDS
    for i in range(int(input())):
        cards_input = input().split()
        location = cards_input[0]
        cards = Cards(cards_input[1:])

        if location == "HAND":
            me.hand = cards
        elif location == "DRAW":
            me.draw = cards
        elif location == "DISCARD":
            me.discard = cards
        elif location == "AUTOMATED":
            me.auto = cards

        elif location == "OPPONENT_CARDS":
            foe.cards = cards
        elif location == "OPPONENT_AUTOMATED":
            foe.auto = cards
        else:
            raise ValueError("Unexpected card location")

    # ACTIONS
    actions = [input() for _ in range(int(input()))]

    # Debug
    print_info(phase, actions, apps, me, foe)

    # Action
    move = play(phase, actions, apps, me, foe)
    print(move)
