import sys
import math


def manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

# width: size of the grid
# height: top left corner is (x=0, y=0)
width, height = [int(i) for i in input().split()]
for i in range(height):
    row = input()  # one line of the grid: space " " is floor, pound "#" is wall


# game loop
turn = 0
while True:
    pacs_mine = []
    pacs_their = []

    my_score, opponent_score = [int(i) for i in input().split()]
    visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
    for i in range(visible_pac_count):
        # pac_id: pac number (unique within a team)
        # mine: true if this pac is yours
        # x: position in the grid
        # y: position in the grid
        # type_id: unused in wood leagues
        # speed_turns_left: unused in wood leagues
        # ability_cooldown: unused in wood leagues
        pac_id, mine, x, y, type_id, speed_turns_left, ability_cooldown = input().split()
        pac_id = int(pac_id)
        point = (int(x), int(y))

        if mine == "1":
            pacs_mine.append(point)
        else:
            pacs_their.append(point)

        speed_turns_left = int(speed_turns_left)
        ability_cooldown = int(ability_cooldown)
    visible_pellet_count = int(input())  # all pellets in sight
    
    super_pellets = []
    normal_pellets = []

    for i in range(visible_pellet_count):
        # value: amount of points this pellet is worth
        x, y, value = [int(j) for j in input().split()]
        if value == 10:
            super_pellets.append((x, y))
        else:
            normal_pellets.append((x,y))
    
    moves = []
    speeds = []
    for p, pac in enumerate(pacs_mine):
        if len(super_pellets) > 0:
            targets = super_pellets
        else:
            targets = normal_pellets

        min_distance = math.inf
        for i, target in enumerate(targets):
            distance = manhattan(pac, target)
            if distance <= min_distance:
                min_distance = distance
                index = i
        moves.append(f"MOVE {p} {targets[index][0]} {targets[index][1]}")        
        speeds.append(f"SPEED {p}")
    
    if turn % 10 == 0:
        print("|".join(speeds))
    else:
        print("|".join(moves))
    
    turn += 1

