import sys
import math


def get_scene():
    # width: size of the grid
    # height: top left corner is (x=0, y=0)
    width, height = [int(i) for i in input().split()]
    scene_dict = {'width': width, 'height': height, 'rows': []}

    for i in range(height):
        # space " " is floor, pound "#" is wall
        scene_dict['rows'].append(input())
    return scene_dict

def get_pacs():
    pacs_mine = []
    pacs_their = []

    for _ in range(visible_pac_count):
        # pac_id: pac number (unique within a team)
        # mine: true if this pac is yours
        # x: position in the grid
        # y: position in the grid
        # type_id: unused in wood leagues
        # speed_turns_left: unused in wood leagues
        # ability_cooldown: unused in wood leagues
        pac_id, mine, x, y, type_id, speed_turns_left, ability_cooldown = input().split()
 
        new_pac = {
            'id': pac_id,
            'position': (int(x), int(y)),
            'type_id': type_id,
            'speed_turns_left': int(speed_turns_left),
            'ability_cooldown': int(ability_cooldown)
        }

        if mine == "1":
            pacs_mine.append(new_pac)
        else:
            pacs_their.append(new_pac)
    return pacs_mine, pacs_their


def calc_distance(p1, p2, width):
    # Manhattan distance
    x_distance = abs(p1[0] - p2[0])
    y_distance = abs(p1[1] - p2[1])
    direct = x_distance + y_distance
    indirect = width - x_distance + y_distance + 1
    return min(direct, indirect)


def calc_p2s_distances(pacs, targets, width):
    all_distances = []
    for pac in pacs_mine:
        targets_distances = []
        for target in targets:
            distance = calc_distance(pac['position'], target, width)
            targets_distances.append({target: distance})
        all_distances.append({'pac_id': pac['id'], 'distances': targets_distances})
    return all_distances


scene = get_scene() 


# game loop
turn = 0
while True:
    pacs_mine = []
    pacs_their = []

    my_score, opponent_score = [int(i) for i in input().split()]
    visible_pac_count = int(input())  # all your pacs and enemy pacs in sight

    pacs_mine, pacs_their = get_pacs()

    visible_pellet_count = int(input())  # all pellets in sight
    
    super_pellets = []
    normal_pellets = []

    for i in range(visible_pellet_count):
        # value: amount of points this pellet is worth
        x, y, value = [int(j) for j in input().split()]
        if value == 10:
            super_pellets.append((x, y))
        else:
            normal_pellets.append((x, y))

 
    # Phase 1 - Super pellets
    if len(super_pellets) > 0:

        # Calculate the distance matrix
        p2s_distances = calc_p2s_distances(pacs_mine, super_pellets, scene['width'])

        print(p2s_distances, file=sys.stderr)


    # Phase 2 - Normal pellets
    else:
        pass

    pac_targets = []

    # Command generation
    moves = []
    speeds = []
    ## print(pac_targets, file=sys.stderr)
    for p, pac_target in enumerate(pac_targets):
        moves.append(f"MOVE {p} {pac_target[0]} {pac_target[1]}")
    
    for p, pac in enumerate(pacs_mine):
        speeds.append(f"SPEED {p}")


    # Turn handler
    if turn % 10 == 0:
        print("|".join(speeds))
    else:
        print("|".join(moves))
    
    turn += 1

