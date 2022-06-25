import sys
from typing import Optional


app_header = f"0  1  2  3  4  5  6  7"

cards_header = f"[0, 1, 2, 3, 4, 5, 6, 7, B, D]"

def debug(msg):
    print(msg, file=sys.stderr, flush=True) 


def output_list(a_list):
    if isinstance(a_list[0], str):
        return '  '.join([x for x in a_list if x])
    elif isinstance(a_list[0], int):
        max_len = max([len(str(x)) for x in a_list])
        return ' '.join([f"{str(x): >2}" for x in a_list])


class Cards():
    def __init__(self, inputs_list: list):
        # Convert to int
        inputs = list(map(int, inputs_list))

        # Main inputs
        self.train, self.code, self.daily, self.tasks, self.arch, self.cd, self.cr, self.ref = inputs[:8]

        # Optional inputs
        inludes_optionals = len(inputs) == 10
        self.bonus = inputs[8] if inludes_optionals else None
        self.debt = inputs[9] if inludes_optionals else None

        self.text = [
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

        self.main = [
            self.train,
            self.code,
            self.daily,
            self.tasks,
            self.arch,
            self.cd,
            self.cr,
            self.ref,
        ]

        self.full = [
            self.train,
            self.code,
            self.daily,
            self.tasks,
            self.arch,
            self.cd,
            self.cr,
            self.ref,
            self.bonus,
            self.debt,
        ]
    
    def __repr__(self):
        return f"{self.full}"


class App():
    def __init__(self, inputs: list):
        self.object_type = inputs[0]
        assert self.object_type == "APPLICATION"
        
        self._id = inputs[1]
        self.specs: Cards = Cards(inputs[2:])

    def __repr__(self):
        return f"{self._id: >2} {output_list(self.specs.main)}"

    def __eq__(self, other):
        return self._id == other._id

    def __lt__(self, other):
        return int(self._id) < int(other._id)


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

        # The deficit for every app
        self.deficit: dict = {}

    def __repr__(self):
        return f"at {self.loc}  score {self.score}  PERM: daily {self.daily}  arch {self.arch}"

    def calc_deficit(self, apps) -> None:
        """
        Calculate the deficit of the player's hand based on the available applications
        """
        if self.hand is None:
            own = 8 * [0]
        else:
            own = self.hand.main

        for app in sorted(apps):
            cards = Cards([spec - resource for spec, resource in zip(app.specs.main, own)])
            self.deficit[app._id] = cards
            debug(f"{app._id: <2} {output_list(cards.main)}")


def print_info(phase, actions, apps, me, foe):
    
    def format_cards(values):
        return values if values else 10 * [0]

    app_title = f"    {app_header}"
    cards_title = f"      {cards_header}"

    debug(f"PHASE: {phase}")
    debug(f"ACTIONS: {output_list(actions)}")

    debug("")
    
    debug("APPS")
    debug(app_title)
    for app in sorted(apps):
        debug(f"{app}")
    debug(app_title)

    debug("")

    debug(f"   ME: {me}")
    debug(cards_title)
    debug(f" HAND: {me.hand}")
    debug(f" DRAW: {me.draw}")
    debug(f" DISC: {format_cards(me.discard)}")
    debug(f" AUTO: {format_cards(me.auto)}")

    debug("")

    debug(f"  FOE: {foe}")
    debug(cards_title)
    debug(f"CARDS: {format_cards(foe.cards)}")
    debug(f" AUTO: {format_cards(foe.auto)}")

    debug("")


def play(phase, actions, apps, me, foe):
    # In the first league: RANDOM | MOVE <zoneId> | RELEASE <applicationId> | WAIT
    #
    # In later leagues: | GIVE <cardType> | THROW <cardType> | TRAINING | CODING | DAILY_ROUTINE 
    #                   | TASK_PRIORITIZATION <cardTypeToThrow> <cardTypeToTake> | ARCHITECTURE_STUDY 
    #                   | CONTINUOUS_DELIVERY <cardTypeToAutomate> | CODE_REVIEW | REFACTORING

    # Check if there is immediately releasable software
    
    debug("MY DEFICITS")
    me.calc_deficit(apps)
    debug("")
    debug("FOE DEFICITS")
    foe.calc_deficit(apps)
    
    return "RANDOM"

# game loop
while True:
    # PHASE
    phase = input()  # can be MOVE, GIVE_CARD, THROW_CARD, PLAY_CARD or RELEASE
    
    # APPS
    apps = [App(input().split()) for _ in range(int(input()))]

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
    action = play(phase, actions, apps, me, foe)
    print(action)
