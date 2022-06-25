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
        return ' '.join([f"{str(x): >2}" for x in a_list])

class CardType():
    def __init__(self, quantity, unit):
        self.quantity = quantity
        self.unit = unit
        self.value = quantity * unit


class Specs():
    def __init__(self, inputs_list: list):
        # Convert to int
        inputs = list(map(int, inputs_list))

        self.train = inputs[0]
        self.code = inputs[1]
        self.daily = inputs[2]
        self.tasks = inputs[3]
        self.arch = inputs[4]
        self.cd = inputs[5]
        self.cr = inputs[6]
        self.ref = inputs[7]

        self.all = [
            self.train,
            self.code,
            self.daily,
            self.tasks,
            self.arch,
            self.cd,
            self.cr,
            self.ref,
        ]

    def get_sum(self):
        return sum(self.all)


class Cards():
    def __init__(self, inputs_list: list):
        # Convert to int
        inputs = list(map(int, inputs_list))

        # Main inputs
        self.train = CardType(inputs[0], 2)
        self.code = CardType(inputs[1], 2)
        self.daily = CardType(inputs[2], 2)
        self.tasks = CardType(inputs[3], 2)
        self.arch = CardType(inputs[4], 2)
        self.cd = CardType(inputs[5], 2)
        self.cr = CardType(inputs[6], 2)
        self.ref = CardType(inputs[7], 2)

        # Optional inputs
        inludes_optionals = len(inputs) == 10
        self.bonus = CardType(inputs[8], 2) if inludes_optionals else CardType(0, 1)
        self.debt = CardType(inputs[9], 2) if inludes_optionals else CardType(0, -1)

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
        return f"{[x.value for x in self.full]}"


class App():
    def __init__(self, inputs: list):
        self.object_type = inputs[0]
        assert self.object_type == "APPLICATION"
        
        self._id = inputs[1]
        self.specs: Specs = Specs(inputs[2:])
        self.difficulty = self.specs.get_sum()

    def __repr__(self):
        return f"{self._id: >2} {output_list(self.specs.all)}"

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

        # Common cards
        self.auto: Optional[Cards] = None

    def __repr__(self):
        return f"at {self.loc}  score {self.score}  PERM: daily {self.daily}  arch {self.arch}"


class Me(Player):
    def __init__(self, inputs_str):
        super().__init__(inputs_str)
        
        # Cards
        self.hand: Optional[Cards] = None
        self.draw: Optional[Cards] = None
        self.discard: Optional[Cards] = None

        # The deficit for every app
        self.deficit: dict = {}

    def calc_deficit(self, apps) -> None:
        """
        Calculate the deficit of the player's hand based on the available applications
        """

        for app in sorted(apps):
            specs = app.specs.all
            hand = [x.quantity for x in self.hand.main]
            deficit = [spec - resource for spec, resource in zip(specs, hand)]
            self.deficit[app._id] = Specs(deficit)

            debug(f"{app._id: >2}: {output_list(deficit)}")


class Foe(Player):
    def __init__(self, inputs_str):
        super().__init__(inputs_str)

        # Cards
        self.cards: Optional[Cards] = None


def print_info(phase, actions, apps, me, foe):
    
    def format_cards(values):
        return values if values else 10 * [0]

    app_title = f"    {app_header}"
    cards_title = f"       {cards_header}"

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

def calc_deficits(me, foe, apps):
    debug("MY DEFICITS")
    me.calc_deficit(apps)
    debug("")
    # debug("FOE DEFICITS")
    # foe.calc_deficit(apps)

def move(me, foe, apps):
    
    # Get a card that is needed for immediate release 
    # if there are more than one immediate release target the one with the max needs
    for app_id, deficit in me.deficit.items():
        debug(f"{app_id}: {deficit.all}")

    # Get a rare card that our opponents needs the most

    # Get a rare card that we need the most

    # Get a card that fullfils the need for the maximum number of apps

    # Get a card the is needed for the most of the apps

    # Get a bonus card
    pass

def release(me, foe, apps):
    
    # Check if there is immediately releasable software
    pass

def play(phase, actions, apps, me, foe):
    # In the first league: RANDOM | MOVE <zoneId> | RELEASE <applicationId> | WAIT
    #
    # In later leagues: | GIVE <cardType> | THROW <cardType> | TRAINING | CODING | DAILY_ROUTINE 
    #                   | TASK_PRIORITIZATION <cardTypeToThrow> <cardTypeToTake> | ARCHITECTURE_STUDY 
    #                   | CONTINUOUS_DELIVERY <cardTypeToAutomate> | CODE_REVIEW | REFACTORING

    # This are the calcs needed for all phases
    calc_deficits(me, foe, apps)

    out = None
    if phase == "MOVE":
        out = move(me, foe, apps)
    elif phase == "RELEASE":
        out = release(me, foe, apps)
    
    print(out or "RANDOM")

def read_inputs():
    # PHASE
    phase = input()  # can be MOVE, GIVE_CARD, THROW_CARD, PLAY_CARD or RELEASE
    
    # APPS
    apps = [App(input().split()) for _ in range(int(input()))]

    # PLAYERS
    me = Me(input())
    foe = Foe(input())

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

    return  phase, actions, apps, me, foe

# game loop
while True:

    phase, actions, apps, me, foe = read_inputs()

    print_info(phase, actions, apps, me, foe)

    play(phase, actions, apps, me, foe)
