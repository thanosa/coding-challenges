import copy
import itertools
import math
import random
import sys

# Constants
SUPER_PELLET_VALUE = 10
MAX_SPEED_TURNS = 5
WALL_CHARACTER = "#"
FLOOR_CHARACTER = " "

MIN_DISTANCE_TO_UNSTUCK = 6
MAX_RANDOM_TRIES = 10


def pr(variable_name, variable):
    """
    This is used to print out the value and the name of a variable.
    """
    print(f"{variable_name}: {variable}", file=sys.stderr)


def next_to(point, direction):
    """
    Gets a point and returns the next on the direction specified.
    """
    assert direction in ['up', 'down', 'left', 'right']

    if direction == 'up':
        return (point[0] - 1, point[1])
    elif direction == 'down':
        return (point[0] + 1, point[1]) 
    elif direction == 'left':
        return (point[0], point[1] - 1) 
    elif direction == 'right':
        return (point[0], point[1] + 1)


def read_scene():
    """
    Reads the scene.
    '#' represents wall
    ' ' represents floor
    The top left corner is the (x=0, y=0)
    """
    width, height = [int(i) for i in input().split()]
    scene = {'width': width, 'height': height, 'rows': [], 'floor': [], 'wall': [], 'loops': []}

    for y in range(height):
        row = input()
        scene['rows'].append(row)

        # Find the floor.
        scene['floor'].extend([(x, y) for x, c in enumerate(row) if c == FLOOR_CHARACTER])
        scene['wall'].extend([(x, y) for x, c in enumerate(row) if c == WALL_CHARACTER])

        pr("row", row)
        # Find the loops.
        if row[0] == row[-1] == FLOOR_CHARACTER:
            scene['loops'].append(y)

    # Collection of all unexplored floor positions.
    scene['unexplored'] = copy.deepcopy(scene['floor'])

    # Analyze scene to detect the pois (points of interest).
    loop_entries = [(x, y) for x in [0, width - 1] for y in scene['loops']]

    # Detect the dead ends.
    dead_ends = []
    for floor in scene['floor']:
        if floor not in loop_entries:
            up = next_to(floor, 'up') in scene['wall']
            down = next_to(floor, 'down') in scene['wall']
            left = next_to(floor, 'left') in scene['wall']
            right = next_to(floor, 'right') in scene['wall']

            # Tricky way to convert a boolean to 0 or 1.
            wall_count = up * 1 + down * 1 + left * 1 + right * 1

            if wall_count == 3:
                dead_ends.append(floor) 
    scene['dead_ends'] = dead_ends

    # Detect the pois (point of interest)
    # These are the floor with 4 liberties, 3 or 2 but in corner.
    # floor_4 = []
    # floor_3 = []
    # floor_2 = []
    # for floor in scene['floor']:
    #     if floor not in [loop_entries, dead_ends]:


    return scene


def read_pacs():
    """
    Read the pacs information.
    """

    pacs = {'mine': [], 'their': []}
    
    # Count the pacs
    pac_count = int(input()) 

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
            pacs['mine'].append(new_pac)
        else:
            pacs['their'].append(new_pac)

    return pacs


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


def update_unexplored(scene, pacs):
    """
    Updates the floor by eliminating the visited floor positions by any pac.
    """
    # Current positions of all pacs.
    pac_positions = [x['position'] for x in pacs['mine'] + pacs['their']]

    # Remove the current pac positions from the floor.
    scene['unexplored'] = [x for x in scene['unexplored'] if x not in pac_positions]

    return scene


def calc_distance(point1, point2, scene):
    """
    Heuristic function to calculate the distance between two targets.
    It is based on the Manhattan distance.
    It is refined to consider the wrap of the scene with the indirect.
    For each of the two points we find the loop that will be used in case of wrap.
    This is the one that has the closest y.
    The vertical distance is the sum of vertical distances of each of the point with the loop 
    """
    dx = abs(point1[0] - point2[0])
    dy = abs(point1[1] - point2[1])
    direct = dx + dy

    if scene['loops'] is not None:
        horizontal = scene['width'] - dx

        min_distances = []
        for point in [point1, point2]:
            min_dy = math.inf
            for loop_y in scene['loops']:
                dy = abs(point[1] - loop_y)
                if dy < min_dy:
                    min_dy = dy
                    closest_loop = loop_y
            min_distances.append(min_dy)
        assert len(min_distances) == 2

        vertical = sum(min_distances) 
        indirect = horizontal + vertical
    else:
        indicect = math.inf

    return min(direct, indirect)


def calc_p2t_distances(pacs, targets, scene):
    """
    Calculates the pac to target distances.
    Currently not used.
    """
    all_distances = []
    for pac in pacs:
        distances = []
        for target in targets:
            distance = calc_distance(pac['position'], target, scene)
            distances.append({target: distance})
        all_distances.append({'pac_id': pac['id'], 'distances': distances})

    return all_distances


def calc_t2t_distances(targets, scene):
    """
    Calculates the target to target distances.
    """
    distances_set = set()
    distances_dict = {}
    for t1, t2 in itertools.combinations(targets, 2):
        distance = calc_distance(t1, t2, scene)
        distances_set.add(distance)
        distances_dict[(t1, t2)] = distance
    
    distances_sorted_set = sorted(distances_set, reverse=True)

    return distances_sorted_set, distances_dict


def calc_clusters(targets, pac_count, scene):
    """
    The number of clusters should not be more than my pacs.
    """
    # Initialize the clusters as one-to-one with the targets.
    clusters = [[x] for x in targets]

    print(f"target: {len(targets)}, pacs: {pac_count}", file=sys.stderr)

    if len(clusters) > pac_count:
        print(f"pac, clusters count: {pac_count}, {len(clusters)}", file=sys.stderr)
        
        # Calculate the super pellet to super pellet distances.
        distances_set, distances_dict = calc_t2t_distances(targets, scene)

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
    
    print(f"clusters: {clusters}", file=sys.stderr)

    return clusters


def collect_super_pellets(pacs, super_pellets, last, scene):
    """
    Collects the super pellets as first priority
    """

    if len(super_pellets) > 0:
        # There is no plan or super pellets have been captured.
        there_is_no_super_pellet_plan = last['super_pellet_plan'] == None
        super_pellets_decreased = len(super_pellets) < last['super_pellet_count']

        if there_is_no_super_pellet_plan or super_pellets_decreased:
            print("collect super pellet - NEW PLAN", file=sys.stderr)
            return plan_super_pellets(pacs['mine'], super_pellets, scene)
        else:
            print("collect super pellet - USE LAST", file=sys.stderr)
            return last['super_pellet_plan']
    

def plan_super_pellets(pacs_mine, targets, scene):
    """
    The planning is done the first time and it is updated only if the count of the 
    super pallets is decreased.

    The super pellets are clustered one by one until they reach the number of pacs.
    Each cluster is assigned to the closest pac and that pac will move to the closest 
    supper pellet of the assigned cluster.

    """

    # Preparation: Cluster the super pellets.
    clusters = calc_clusters(targets, len(pacs_mine), scene)
    assert len(pacs_mine) >= len(clusters)

    # Assign a pac to each cluster.
    
    # Create saved deep copies.
    clusters_saved = copy.deepcopy(clusters)

    pac_targets = {}

    for cluster in clusters:

        min_distance = math.inf
        selected_pac = None
        selected_cluster = None
        selected_target = None

        for target in cluster:
            for pac in pacs_mine:
                distance = calc_distance(pac['position'], target, scene)
                if distance < min_distance:
                    min_distance = distance
                    selected_pac = pac
                    selected_cluster = cluster
                    selected_target = target

        assert selected_pac is not None
        assert selected_cluster is not None
        assert selected_target is not None

        # Assign the target to the pac.   
        pac_targets[selected_pac['id']] = selected_target

        # Remove the assigned pac.
        pacs_mine = [x for x in pacs_mine if not (x.get('id') == selected_pac['id'])]

        # Remove the assigned cluster.
        clusters = [x for x in clusters if not x == selected_cluster]

    return pac_targets


def resolve_stucks(current_pacs, last, scene):
    """
    Basic way to unstuck my packs in case they stay on the same square floor.
    The detection should consider the speed up (speed_turns_left': 5)
    """
    last_pacs = last['pacs_mine']

    pac_to_unstuck = {}
    unexplored = scene['unexplored']

    for pac_now in current_pacs:
        for pac_last in last_pacs:
            if pac_now['position'] == pac_last['position'] and pac_now['speed_turns_left'] != MAX_SPEED_TURNS:
                if len(unexplored) > 0:
                    # Choose the first random unexplored floor that further than threshold.
                    print("CASE1", file=sys.stderr)
                    chosen = None
                    for _ in range(MAX_RANDOM_TRIES):
                        random_floor = random.choice(unexplored)
                        distance = calc_distance(pac_now['position'], random_floor, scene)

                        if distance > MIN_DISTANCE_TO_UNSTUCK:
                            chosen = random_floor
                            break
                    
                    # If nothing has been chosen, a random one is chosen.
                    if chosen == None:
                        print("CASE2", file=sys.stderr)
                        chosen = random.choice(unexplored)
                else:
                    # If there is no unexplored ares then select a random floor.
                    print("CASE3", file=sys.stderr)
                    chosen = random.choice(scene['floor'])

                pac_to_unstuck[pac_now['id']] = chosen

    return pac_to_unstuck


def find_available_pacs(pacs, pac_to_super, pac_to_unstuck=None, pac_to_normal=None):
    """
    Finds the available pacs that are not assigned
    """

    # for pac in pacs['mine']:
    #     print(f"pac mine: {pac}", file=sys.stderr)
    # print(f"pac_to_super  : {pac_to_super}", file=sys.stderr)
    # print(f"pac_to_unstuck: {pac_to_unstuck}", file=sys.stderr)
    # print(f"pac_to_normal : {pac_to_normal}", file=sys.stderr)

    available_pacs = pacs['mine']

    if pac_to_super is not None:
        available_pacs = [x for x in pacs['mine'] if x['id'] not in pac_to_super.keys()]

    if pac_to_unstuck is not None:
        available_pacs = [x for x in available_pacs if x['id'] not in pac_to_unstuck.keys()]
    
    if pac_to_normal is not None:
        available_pacs = [x for x in available_pacs if x['id'] not in pac_to_normal.keys()]

    print(f"available_pacs: {available_pacs}", file=sys.stderr)

    return available_pacs


def plan_normal_pellets(pacs_mine, targets, scene):
    """
    Each pac is assgined to the closest available normal pellet
    """

    print(f"normal pellets: {targets}", file=sys.stderr)

    pac_targets = {}

    # Assign each pac to the closes normal pellet.
    if pacs_mine is not None:
        for pac in pacs_mine:
            min_distance = math.inf
            selected_target = None
            for target in targets:
                distance = calc_distance(pac['position'], target, scene)
                if distance < min_distance:
                    min_distance = distance
                    selected_target = target
            
            if selected_target is not None:
                # Assign the target to the pac.   
                pac_targets[pac['id']] = selected_target

                # Remove the assigned target.
                targets = [x for x in targets if not x == selected_target]

    return pac_targets


def explore_floor(pacs_mine, scene):
    """
    The pacs are sent the most distant floor of the unexplored area.
    """
    pac_target = {}
    
    unexplored = scene['unexplored']

    if len(unexplored) > 0:
        targets = unexplored
        for pac in pacs_mine:
            min_distance = math.inf
            selected_target = None
            for target in targets:
                distance = calc_distance(pac['position'], target, scene)
                if distance < min_distance:
                    min_distance = distance
                    selected_target = target

            assert selected_target is not None

            # Assign the target to the pac.   
            pac_target[pac['id']] = selected_target

            # Remove the assigned target.
            targets = [x for x in targets if not x == selected_target]
    
    return pac_target


def merge_targets(pac_to_super, pac_to_unstuck, pac_to_normal, pac_to_explore):
    """
    Merges the targets dictionaries into a single one.
    """
    pac_targets = {}

    if pac_to_super is not None:
        pac_targets = copy.deepcopy(pac_to_super)

    if pac_to_unstuck is not None:
        pac_targets.update(pac_to_unstuck)

    if pac_to_normal is not None:
        pac_targets.update(pac_to_normal)

    if pac_to_explore is not None:
        pac_targets.update(pac_to_explore)

    return pac_targets


def main():

    # Read the scene.
    scene = read_scene()

    # Initialize the cross turn variables.
    last = {
        'super_pellet_count': -1, 
        'super_pellet_plan': None,
        'pacs_mine': {}}

    # Game loop.
    turn = 0
    while True:

        # Read score.
        score = {}
        score['mine'], score['their'] = [int(i) for i in input().split()]

        # Read pacs.
        pacs = read_pacs()

        # Update the unexplored floor.
        scene = update_unexplored(scene, pacs)

        # Read pellets.
        pellet_count, super_pellets, normal_pellets = read_pellets()

        # Pass 1 - Collect super pellets
        pac_to_super = collect_super_pellets(pacs, super_pellets, last, scene)

        # Pass 2 - Resolve stucks
        available_pacs = find_available_pacs(pacs, pac_to_super)
        pac_to_unstuck = resolve_stucks(available_pacs, last, scene)

        # Pass 3 - Collect normal pellets.
        available_pacs = find_available_pacs(pacs, pac_to_super, pac_to_unstuck)
        pac_to_normal = plan_normal_pellets(available_pacs, normal_pellets, scene)

        # Pass 4 - Exploration of the unexplored floor.
        available_pacs = find_available_pacs(pacs, pac_to_super, pac_to_unstuck, pac_to_normal)
        pac_to_explore = explore_floor(available_pacs, scene)

        # Merge the pac targets.
        print(f"pac to super  : {pac_to_super}", file=sys.stderr)
        print(f"pac to unstack: {pac_to_unstuck}", file=sys.stderr)
        print(f"pac to normal : {pac_to_normal}", file=sys.stderr)
        print(f"pac to explore: {pac_to_explore}", file=sys.stderr)
        pac_targets = merge_targets(pac_to_super, pac_to_unstuck, pac_to_normal, pac_to_explore)

        # Command generation.
        moves = [f"MOVE {pac} {target[0]} {target[1]} ({target[0]},{target[1]})" for pac, target in pac_targets.items()]
        speeds = [f"SPEED {pac['id']}" for pac in pacs['mine']]
       
        # Turn handler.
        if turn % 10 == 0:
            print("|".join(speeds))
        else:
            print("|".join(moves))
        turn += 1

        # Updates of the cross turn variables.
        last['super_pellet_count'] = len(super_pellets)
        last['super_pellet_plan'] = pac_to_super
        last['pacs_mine'] = copy.deepcopy(pacs['mine'])
        
        print(f"last: {last}", file=sys.stderr)


# Entry point.
main()