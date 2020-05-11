import copy
import itertools
import sys
import math

# Constants
SUPER_PELLET_VALUE = 10
WALL = "#"
FLOOR = " "

def read_scene():
    """
    Reads the scene.
    '#' represents wall
    ' ' represents floor
    The top left corner is the (x=0, y=0)
    """
    width, height = [int(i) for i in input().split()]
    scene_dict = {'width': width, 'height': height, 'rows': []}

    floor = []
    for y in range(height):
        row = input()
        scene_dict['rows'].append(row)

        floor.extend([(x, y) for x, c in enumerate(row) if c == FLOOR])

    return scene_dict, floor


def read_pacs():
    """
    Read the pacs information.
    """
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
    """
    Reads the pallet information
    """

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


def update_unexplored_floor(floor, pacs_mine, pacs_their):
    """
    Updates the floor by eliminating the visited floor positions by any pac.
    """

    # Current positions of all pacs.
    pac_positions = [x['position'] for x in pacs_mine + pacs_their]

    # Remove the current pac positions from the floor.
    floor = [x for x in floor if x not in pac_positions]

    return floor


def calc_distance(point1, point2, width):
    """
    Heuristic function to calculate the distance between two targets.
    It is based on the Manhattan distance.
    It is refined to consider the wrap of the scene.
    """
    x_distance = abs(point1[0] - point2[0])
    y_distance = abs(point1[1] - point2[1])
    direct = x_distance + y_distance
    indirect = width - x_distance + y_distance + 1

    return min(direct, indirect)


def calc_p2t_distances(pacs, targets, width):
    """
    Calculates the pac to target distances.
    Currently not used.
    """
    all_distances = []
    for pac in pacs:
        distances = []
        for target in targets:
            distance = calc_distance(pac['position'], target, width)
            distances.append({target: distance})
        all_distances.append({'pac_id': pac['id'], 'distances': distances})

    return all_distances


def calc_t2t_distances(targets, width):
    """
    Calculates the target to target distances.
    """
    distances_set = set()
    distances_dict = {}
    for t1, t2 in itertools.combinations(targets, 2):
        distance = calc_distance(t1, t2, width)
        distances_set.add(distance)
        distances_dict[(t1, t2)] = distance
    
    distances_sorted_set = sorted(distances_set, reverse=True)

    return distances_sorted_set, distances_dict


def calc_clusters(targets, pac_count, width):
    """
    The number of clusters should not be more than my pacs.
    """
    # Initialize the clusters as one-to-one with the targets.
    clusters = [[x] for x in targets]

    if len(clusters) > pac_count:
        print(f"pac, clusters count: {pac_count}, {len(clusters)}", file=sys.stderr)
        
        # Calculate the super pellet to super pellet distances.
        distances_set, distances_dict = calc_t2t_distances(targets, width)

        print(f"unique distances: {distances_set}", file=sys.stderr)
        for d in distances_dict.items():
            print(d, file=sys.stderr)

        # Clustering the targets one-by-one until they become as much as my pacs.
        for _ in range(len(clusters) - pac_count):
            pair_to_join = min(distances_dict, key=(lambda key: distances_dict[key]))
            print(f"pair to join: {pair_to_join}", file=sys.stderr)

            # Update of the distances matrix
            del distances_dict[pair_to_join]

            # Actual merge of the clustering
            clusters = [x for x in clusters if (x[0] != pair_to_join[0]) and (x[0] != pair_to_join[1])]
            clusters.append([x for x in pair_to_join])
    
    return clusters


def collect_super_pellets(pacs_mine, targets, width):
    """
    The planning is done the first time and it is updated only if the count of the 
    super pallets is decreased.

    The super pellets are clustered one by one until they reach the number of pacs.
    Each cluster is assigned to the closest pac and that pac will move to the closest 
    supper pellet of the assigned cluster.

    """

    # Preparation: Cluster the super pellets.
    clusters = calc_clusters(targets, len(pacs_mine), width)
    assert len(pacs_mine) >= len(clusters)

    # Assign a pac to each cluster.
    
    # Create saved deep copies.
    clusters_saved = copy.deepcopy(clusters)

    pac_target = {}

    for cluster in clusters:

        min_distance = math.inf
        selected_pac = None
        selected_cluster = None
        selected_target = None

        for target in cluster:
            for pac in pacs_mine:
                distance = calc_distance(pac['position'], target, width)
                if distance < min_distance:
                    min_distance = distance
                    selected_pac = pac
                    selected_cluster = cluster
                    selected_target = target

        assert selected_pac is not None
        assert selected_cluster is not None
        assert selected_target is not None

        # Assign the target to the pac.   
        pac_target[selected_pac['id']] = selected_target

        # Remove the assigned pac.
        pacs_mine = [x for x in pacs_mine if not (x.get('id') == selected_pac['id'])]

        # Remove the assigned cluster.
        clusters = [x for x in clusters if not x == selected_cluster]

    # The pacs_mine now has the available pacs.
    return pac_target, pacs_mine


def collect_normal_pellets(pacs_mine, targets, width):
    """
    Each pac is assgined to the closest available normal pellet
    """

    print(f"normal pellets: {targets}", file=sys.stderr)

    pac_target = {}

    # Assign each pac to the closes normal pellet.
    for pac in pacs_mine:
        min_distance = math.inf
        selected_target = None
        for target in targets:
            distance = calc_distance(pac['position'], target, width)
            if distance < min_distance:
                min_distance = distance
                selected_target = target
        
        if selected_target is not None:
            # Assign the target to the pac.   
            pac_target[pac['id']] = selected_target

            # Remove the assigned target.
            targets = [x for x in targets if not x == selected_target]

    return pac_target


def explore_floor(pacs_mine, unexplored, width):
    """
    The pacs are sent the most distant floor of the unexplored area.
    """
    pac_target = {}
    
    if len(unexplored) > 0:
        targets = unexplored
        for pac in pacs_mine:
            min_distance = math.inf
            selected_target = None
            for target in targets:
                distance = calc_distance(pac['position'], target, width)
                if distance < min_distance:
                    min_distance = distance
                    selected_target = target

            assert selected_target is not None

            # Assign the target to the pac.   
            pac_target[pac['id']] = selected_target

            # Remove the assigned target.
            targets = [x for x in targets if not x == selected_target]
    
    return pac_target


def main():

    # Read the scene.
    scene, floor = read_scene() 

    # Collection of all unexplored floor positions.
    unexplored = copy.deepcopy(floor)

    # Initialize the cross turn variables.
    last_super_pellet_count = -1
    last_super_pellet_plan = None

    # Game loop.
    turn = 0
    while True:

        # Read score.
        my_score, opponent_score = [int(i) for i in input().split()]

        # Read pacs.
        pacs_mine, pacs_their = read_pacs()

        # Update the unexplored floor.
        unexplored = update_unexplored_floor(unexplored, pacs_mine, pacs_their)

        # Read pellets.
        pellet_count, super_pellets, normal_pellets = read_pellets()

        # Pass 1 - Collect super pellets
        pac_to_super = {}
        if len(super_pellets) > 0:
            # A new plan is done only if there is none  or if a super pellet has been disappered in last turn
            if last_super_pellet_plan == None or len(super_pellets) < last_super_pellet_count:
                pac_to_super, available_pacs = collect_super_pellets(pacs_mine, super_pellets, scene['width'])
            else:
                pac_to_super, available_pacs = collect_super_pellets(pacs_mine, super_pellets, scene['width'])

        # Pass 2 - Collect normal pellets.
        pac_to_normal = {}
        if available_pacs:
            pac_to_normal = collect_normal_pellets(pacs_mine, normal_pellets, scene['width'])

        # TODO only the available pacs should go to explore
        # pac_to_explore = {}


        # Merge the pac targets.
        print(f"pac targets super : {pac_to_super}", file=sys.stderr)
        print(f"pac targets normal: {pac_to_normal}", file=sys.stderr)
        pac_targets = {**pac_to_super, **pac_to_normal}

        # Command generation.
        moves = [f"MOVE {pac} {target[0]} {target[1]} ({target[0]},{target[1]})" for pac, target in pac_targets.items()]
        speeds = [f"SPEED {pac['id']}" for pac in pacs_mine]
       
        # Turn handler.
        if turn % 10 == 0:
            print("|".join(speeds))
        else:
            print("|".join(moves))
        turn += 1

        # Updates of the cross turn variables.
        last_super_pellet_count = len(super_pellets)
        if len(super_pellets) > 0:
            last_super_pellet_plan = pac_to_super

# Entry point.
main()