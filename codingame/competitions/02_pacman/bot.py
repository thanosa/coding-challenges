import itertools
import sys
import math


SUPER_PELLET_VALUE = 10

def read_scene():
    # width: size of the grid
    # height: top left corner is (x=0, y=0)
    width, height = [int(i) for i in input().split()]
    scene_dict = {'width': width, 'height': height, 'rows': []}

    for _ in range(height):
        # space " " is floor, pound "#" is wall
        scene_dict['rows'].append(input())
    return scene_dict


def read_pacs():

    # Count the pacs
    pac_count = int(input()) 

    # Read the pacs
    pacs_mine = []
    pacs_their = []

    for _ in range(pac_count):
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


def read_pellets():

    # Read pellet count
    pellet_count = int(input()) 

    super_pellets = []
    normal_pellets = []

    for _ in range(pellet_count):
        x, y, value = [int(j) for j in input().split()]
        if value == SUPER_PELLET_VALUE:
            super_pellets.append((x, y))
        else:
            normal_pellets.append((x, y))
    return pellet_count, super_pellets, normal_pellets


def calc_distance(p1, p2, width):
    # Manhattan distance
    x_distance = abs(p1[0] - p2[0])
    y_distance = abs(p1[1] - p2[1])
    direct = x_distance + y_distance
    indirect = width - x_distance + y_distance + 1
    return min(direct, indirect)


def calc_p2s_distances(pacs, targets, width):
    all_distances = []
    for pac in pacs:
        distances = []
        for target in targets:
            distance = calc_distance(pac['position'], target, width)
            distances.append({target: distance})
        all_distances.append({'pac_id': pac['id'], 'distances': distances})
    return all_distances


def calc_s2s_distances(targets, width):
    iterator = itertools.combinations(targets, 2)
    distances = {(t1, t2): calc_distance(t1, t2, width) for t1, t2 in iterator}
    return distances


def calc_clusters(s2s_distances, pac_count):
    print(s2s_distances, file=sys.stderr)

    # The number of clusters should not be more than the pacs.
    # # if len(s2s_distances) > pac_count:



def main():
    # Read the scene
    scene = read_scene() 

    # Game loop
    turn = 0
    while True:

        # Read score
        my_score, opponent_score = [int(i) for i in input().split()]

        # Read pacs
        pacs_mine, pacs_their = read_pacs()

        # Read pellets
        pellet_count, super_pellets, normal_pellets = read_pellets()

        # Phase 1 - Super pellets
        if len(super_pellets) > 0:

            # Calculate the pac to super pellet distances
            p2s_distances = calc_p2s_distances(pacs_mine, super_pellets, scene['width'])

            # Calculate the super pellet to super pellet distances
            s2s_distances = calc_s2s_distances(super_pellets, scene['width'])

            # Clusters the super pellets
            super_pellets_clusters = calc_clusters(s2s_distances, len(pacs_mine))

            print(super_pellets_clusters, file=sys.stderr)


        # Phase 2 - Normal pellets
        else:
            pass

        pac_targets = []

        # Command generation
        moves = []
        speeds = []
        for pac in pac_targets:
            moves.append(f"MOVE {pac['id']} {pac['target'][0]} {pac['target'][1]}")
        
        for pac in pacs_mine:
            speeds.append(f"SPEED {pac['id']}")


        # Turn handler
        if turn % 10 == 0:
            print("|".join(speeds))
        else:
            print("|".join(moves))
        turn += 1


# Entry point
main()