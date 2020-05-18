import copy
import itertools
import math
import random
import sys

from statistics import median

# Constants
SUPER_PELLET_VALUE = 10
MAX_SPEED_TURNS = 5
WALL_CHARACTER = "#"
FLOOR_CHARACTER = " "

# Globals
COMMANDS = None

# Configuration
MIN_DISTANCE_TO_UNSTUCK = 6
MAX_RANDOM_TRIES = 10
MAX_LOOP_TRIES = 20
FLOOR_4_PERCENTAGE_THRESHOLD = 0.6
FLOOR_3_PERCENTAGE_THRESHOLD = 0.7
FLOOR_2_PERCENTAGE_THRESHOLD = 0.8
GAME_MATURITY_FOR_SPEEDS = -0.40
MAX_PROXIMITY_TO_SWITCH = 7
MAX_PROXIMITY_TO_HUNT = 2
MAX_DISTANCE_TO_SPEED = 5
MIN_PEACE_TO_SPEED = 8


def pr(message, variable=None):
    """
    Shortcut to print out a message and optionaly the value of a variable .
    """
    if variable is not None:
        print(f"{message}: {variable}", file=sys.stderr)
    else:
        print(f"{message}", file=sys.stderr)


def get_neighbors(point, direction=None) -> {}:
    """
    Gets a point and returns all directions or one specified.
    """
    neighbors = { 
        'up': (point[0] - 1, point[1]),
        'down': (point[0] + 1, point[1]),
        'left': (point[0], point[1] - 1),
        'right': (point[0], point[1] + 1)}

    if direction is None:
        return neighbors
    else:
        assert direction in ['up', 'down', 'left', 'right']
        return neighbors[direction]


def calc_pacs_proximity(pac1, pac2, pacs, scene) -> int:
    """
    Calcualtes the proximity between two pacs.
        -1: Pacs are not seeing each other
         0: Pacs are face-to-face
       N>0: Pacs see each other with N floor in between them.

       Loops are not taken into consideration as confronting 
       exacting on a loop door is rare.
    """
    my_pac_positions = {x['position'] for x in pacs['mine']}
    their_pac_positions = {x['position'] for x in pacs['their']}
    obstacles = scene['wall'] | my_pac_positions | their_pac_positions

    horizontal = pac1[1] == pac2[1]
    vertical = pac1[0] == pac2[0]

    # The are not in the same row or column.
    if not horizontal and not vertical:
        return -1
    elif horizontal:
        y = pac1[1]
        min_x = min(pac1[0], pac2[0])
        max_x = max(pac1[0], pac2[0])

        # They are face-to-face.
        floor_in_between = (max_x - min_x) - 1
        if floor_in_between == 0:
            return floor_in_between
        else:
            # Check for obstacles.
            for x in range(min_x + 1, max_x):
                if (x, y) in obstacles:
                    return -1
            return floor_in_between
    elif vertical:
        x = pac1[0]
        min_y = min(pac1[1], pac2[1])
        max_y = max(pac1[1], pac2[1])

        # They are next to each other.
        floor_in_between = (max_y - min_y) - 1
        if floor_in_between == 0:
            return floor_in_between
        else:
            # Check for obstacles.
            for y in range(min_y + 1, max_y):
                if (x, y) in obstacles:
                    return -1
            return floor_in_between


def calc_pellets_proximity(pac_mine_position, normal_pellet, scene) -> int:
    """
    Calculates the proximity between a pac and a pellet.
        -1: Pac is not seeting the pellet
         0: Pac is face to face with the pellet
       N>0: Pac sees the pellet and there are N floor in between them.
    """
    obstacles = scene['wall'] 

    horizontal = pac_mine_position[1] == normal_pellet[1]
    vertical = pac_mine_position[0] == normal_pellet[0]

    # The are not in the same row or column.
    if not horizontal and not vertical:
        return -1, ""
    elif horizontal:
        y = pac_mine_position[1]
        min_x = min(pac_mine_position[0], normal_pellet[0])
        max_x = max(pac_mine_position[0], normal_pellet[0])

        # Find the direction
        if pac_mine_position[0] > normal_pellet[0]:
            direction = "left"
        else:
            direction = "right"

        # They are face-to-face.
        floor_in_between = (max_x - min_x) - 1
        if floor_in_between == 0:
            return floor_in_between, direction
        else:
            # Check if it is on loop entry
            if pac_mine_position in scene['loop_entries'] and normal_pellet in scene['loop_entries']:
                if pac_mine_position[0] == 0:
                    return 0, "left"
                else:
                    return 0, "right"

            # Check for obstacles.
            for x in range(min_x + 1, max_x):
                if (x, y) in obstacles:
                    return -1, ""
            return floor_in_between, direction
    elif vertical:
        x = pac_mine_position[0]
        min_y = min(pac_mine_position[1], normal_pellet[1])
        max_y = max(pac_mine_position[1], normal_pellet[1])

        # Find the direction
        if pac_mine_position[1] > normal_pellet[1]:
            direction = "up"
        else:
            direction = "down"

        # They are next to each other.
        floor_in_between = (max_y - min_y) - 1
        if floor_in_between == 0:
            return floor_in_between, direction
        else:
            # Check for obstacles.
            for y in range(min_y + 1, max_y):
                if (x, y) in obstacles:
                    return -1, ""
            return floor_in_between, direction


def play_rps(pac_mine_type, pac_their_type) -> int:
    """
    Return the outcome of the Rock Papper Scissors game.
         1: win
         0: tie
        -1: lose
    """
    if pac_mine_type == pac_their_type:
        return 0
    elif pac_mine_type == "ROCK":
        if pac_their_type == "SCISSORS":
            return 1
        else:
            return "LOSE"
    elif pac_mine_type == "PAPER":
        if pac_their_type == "ROCK":
            return 1
        else:
            return "LOSE"
    elif pac_mine_type == "SCISSORS":
        if pac_their_type == "PAPER":
            return 1
        else:
            return -1


def advice_rps(pac_their_type) -> str:
    """
    Gets a pac type and returns the one that wins it.
    """
    assert pac_their_type in ["ROCK", "PAPER", "SCISSORS"]

    if pac_their_type == "ROCK":
        return "PAPER"
    elif pac_their_type == "PAPER":
        return "SCISSORS"
    elif pac_their_type == "SCISSORS":
        return "ROCK"


def middle_element(values):
    """
    Returns the middle element from a lust.
    In case the number of values are even, the biggest one is discarted.
    """

    if len(values) % 2 == 0:
        values = values[:-1]

    return median(values)


def read_scene():
    """
    Reads the scene.
    '#' represents wall
    ' ' represents floor
    The top left corner is the (x=0, y=0)
    """
    width, height = [int(i) for i in input().split()]
    scene = {'width': width, 'height': height, 'rows': [], 
             'floor': set(), 'floor_4': set(), 'floor_3': set(), 'floor_2_corner': set(), 'floor_2_aisle': set(), 'floor_1': set(),
             'un_floor': set(), 'un_floor_4': set(), 'un_floor_3': set(), 'un_floor_2_corner': set(), 'un_floor_2_aisle': set(), 'un_floor_1': set(),
             'wall': set(), 'loops': set(), 'loop_entries': set(), 
             'escape': {}}

    for y in range(height):
        row = input()
        scene['rows'].append(row)

        # Detect floor and wall.
        scene['floor'] |= {(x, y) for x, c in enumerate(row) if c == FLOOR_CHARACTER}
        scene['wall'] |= {(x, y) for x, c in enumerate(row) if c == WALL_CHARACTER}

        # Detect loops entries.
        if row[0] == row[-1] == FLOOR_CHARACTER:
            scene['loops'].add(y)
            scene['loop_entries'] |= {(0, y), (width - 1, y)}

    # Analyze floor liberties
    # 4 liberties: crossroad
    # 3 liberties: T-shaped crossroad
    # 2 liberties: corners or aisles
    # 1 liberty:   dead-end
    for floor in scene['floor'].difference(scene['loop_entries']):
        neighbors = get_neighbors(floor)
        
        liberties = sum([1 if neighbor in scene['floor'] else 0 for neighbor in neighbors.values()])
        
        if liberties == 4:
            scene['floor_4'].add(floor)
        elif liberties == 3:
            scene['floor_3'].add(floor)
        elif liberties == 2:
            is_vertical = neighbors['up'] in scene['floor'] and neighbors['down'] in scene['floor']
            is_horizontal = neighbors['left'] in scene['floor'] and neighbors['right'] in scene['floor']
            if is_vertical or is_horizontal:
                scene['floor_2_aisle'].add(floor)
            else:
                scene['floor_2_corner'].add(floor)
        elif liberties == 1:
            scene['floor_1'].add(floor)

    # Find 4 escape floors.
    #
    # Constants.
    most_left_x = 1
    most_right_x = scene['width'] - 2
    most_up_y = 1
    most_down_y = scene['height'] - 2
    
    # Temporary dictionary with the floor that sits on the sides.
    sides = {}

    # Left most.
    side = "left"
    sides[side] = set()
    for floor in scene['floor']:
        if floor[0] == most_left_x:
            sides[side].add(floor)
    y_values = [v[1] for v in sides[side]]
    y_median = middle_element(y_values)
    scene['escape'][side] = (most_left_x, y_median)
    
    # Right most.
    side = "right"
    sides[side] = set()
    for floor in scene['floor']:
        if floor[0] == most_right_x:
            sides[side].add(floor)
    y_values = [v[1] for v in sides[side]]
    y_median = middle_element(y_values)
    scene['escape'][side] = (most_right_x, y_median)

    # Up most.
    side = "up"
    sides[side] = set()
    for floor in scene['floor']:
        if floor[1] == most_up_y:
            sides[side].add(floor)
    x_values = [v[0] for v in sides[side]]
    x_median = middle_element(x_values)
    scene['escape'][side] = (x_median, most_up_y)

    # Down most.
    side = "down"
    sides[side] = set()
    for floor in scene['floor']:
        if floor[1] == most_down_y:
            sides[side].add(floor)
    x_values = [v[0] for v in sides[side]]
    x_median = middle_element(x_values)
    scene['escape'][side] = (x_median, most_down_y)


    # Initialize unexplored floor.
    scene['un_floor'] = copy.deepcopy(scene['floor'])
    scene['un_floor_4'] = copy.deepcopy(scene['floor_4'])
    scene['un_floor_3'] = copy.deepcopy(scene['floor_3'])
    scene['un_floor_2_corner'] = copy.deepcopy(scene['floor_2_corner'])
    scene['un_floor_2_aisle'] = copy.deepcopy(scene['floor_2_aisle'])
    scene['un_floor_1'] = copy.deepcopy(scene['floor_1'])

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
    all_pac_positions = set([x['position'] for x in pacs['mine'] + pacs['their']])
    mine_pac_positions = set([x['position'] for x in pacs['mine']])

    # Remove the current pac positions from the floor.
    scene['un_floor'] = scene['un_floor'].difference(all_pac_positions)

    # Update the pois and dead ends with my positions only.
    scene['un_floor_4'] = scene['un_floor_4'].difference(mine_pac_positions)
    scene['un_floor_3'] = scene['un_floor_3'].difference(mine_pac_positions)
    scene['un_floor_2_corner'] = scene['un_floor_2_corner'].difference(mine_pac_positions)
    scene['un_floor_2_aisle'] = scene['un_floor_2_aisle'].difference(mine_pac_positions)
    scene['un_floor_1'] = scene['un_floor_1'].difference(mine_pac_positions)

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
    The super pellets are clustered one by one until they reach the number of pacs.
    """
    
    print(f"target: {len(targets)}, pacs: {pac_count}", file=sys.stderr)

    # Initialize the clusters as one-to-one with the targets.
    clusters = [[x] for x in targets]

    if len(targets) > pac_count:
        
        # Calculate the super pellet to super pellet distances.
        distances_set, distances_dict = calc_t2t_distances(targets, scene)

        # Clustering the targets one-by-one until they become as much as my pacs.
        for _ in range(len(clusters) - pac_count):
            pair_to_join = min(distances_dict, key=(lambda key: distances_dict[key]))

            # Update of the distances matrix
            del distances_dict[pair_to_join]

            # Find the two clusters the pairs belong to.
            clusters_to_join = []
            for i in range(2):
                for cluster in clusters:
                    if pair_to_join[i] in cluster:
                        clusters_to_join.append(cluster)
                        break
            
            # Create the new cluster
            new_cluster = []
            for cluster in clusters_to_join:
                for floor in cluster:
                    new_cluster.append(floor)
            
            # Remove the individual parts from the existing clusters
            clusters = [x for x in clusters if (x[0] != pair_to_join[0]) and (x[0] != pair_to_join[1])]

            # Add the new cluster to the clusters.
            clusters.append(new_cluster)
    
    return clusters


def collect_super_pellets(pacs_mine, super_pellets, last, scene):
    """
    Collects the super pellets as first priority
    """

    if len(super_pellets) > 0:
        # There is no plan or super pellets have been captured.
        there_is_no_super_pellet_plan = last['super_pellet_plan'] == None
        super_pellets_decreased = len(super_pellets) < last['super_pellet_count']

        if there_is_no_super_pellet_plan or super_pellets_decreased:
            pr("SUPER - CREATE NEW")
            return plan_super_pellets(pacs_mine, super_pellets, scene)
        else:
            pr("SUPER - USE LAST")
            return last['super_pellet_plan']
    

def plan_super_pellets(pacs_mine, super_pellets, scene):
    """
    The plan is done once and is updated only if the count of the 
    super pallets is decreased.

    Each pac is moving to the closest super pellet 
    and the rest super pellets of its cluster are left available.
    """

    # Preparation: Cluster the super pellets.
    clusters = calc_clusters(super_pellets, len(pacs_mine), scene)
    assert len(pacs_mine) >= len(clusters)
    
    # Create saved deep copies.
    clusters_saved = copy.deepcopy(clusters)

    pac_targets = {}

    while clusters:
        min_distance = math.inf
        selected_pac = None
        selected_target = None
        selected_cluster = None


        for target in super_pellets:
            for pac in pacs_mine:
                distance = calc_distance(pac['position'], target, scene)
                if distance < min_distance:
                    min_distance = distance
                    selected_pac = pac
                    selected_target = target
        
        for cluster in clusters:
            if selected_target in cluster:
                selected_cluster = cluster

        assert selected_pac is not None
        assert selected_cluster is not None
        assert selected_target is not None

        # Assign the target to the pac.   
        pac_targets[selected_pac['id']] = selected_target

        # Remove the selected pac.
        pacs_mine = [x for x in pacs_mine if not (x.get('id') == selected_pac['id'])]

        # Remove the selected cluster.
        clusters = [x for x in clusters if not x == selected_cluster]

        # Remove the super pellets that belong to the selected cluster.
        for target in selected_cluster:
            super_pellets.remove(target)

    return pac_targets


def resolve_stucks(current_pacs, last, scene):
    """
    Basic way to unstuck my packs in case they stay on the same square floor.
    The detection should consider the speed up (speed_turns_left': 5)
    """
    last_pacs = last['pacs_mine']

    pac_to_unstuck = {}
    unexplored = scene['un_floor']
    
    for pac_now in current_pacs:
        for pac_last in last_pacs:

            same_position = pac_now['position'] == pac_last['position']
            same_type = pac_now['type_id'] == pac_last['type_id']
            no_max_speed_turns = pac_now['speed_turns_left'] != MAX_SPEED_TURNS

            if same_position and same_type and no_max_speed_turns:
                # Select the most distance escape floor.
                selected_escape = None
                max_distance = -math.inf
                for place, escape in scene['escape'].items():
                    distance = calc_distance(pac_now['position'], escape, scene)
                    if distance > max_distance:
                        max_distance = distance
                        selected_escape = escape
                pac_to_unstuck[pac_now['id']] = selected_escape

    return pac_to_unstuck


def find_available_pacs(pacs, pac_to_unstuck=None, pac_to_super=None, pac_to_normal=None):
    """
    Finds the available pacs that are not assigned
    """

    available_pacs = pacs['mine']

    if pac_to_unstuck is not None:
        available_pacs = [x for x in available_pacs if x['id'] not in pac_to_unstuck.keys()]
    
    if pac_to_super is not None:
        available_pacs = [x for x in available_pacs if x['id'] not in pac_to_super.keys()]
    
    if pac_to_normal is not None:
        available_pacs = [x for x in available_pacs if x['id'] not in pac_to_normal.keys()]

    return available_pacs


def collect_normal_pellets(pacs_mine, normal_pellets, last, scene):
    """
    Each pac is assgined to the closest available normal pellet
    """

    pac_targets = {}

    if pacs_mine is None:
        return pac_targets

    # Assign each pac the furhter available blue that is on the line of sight
    # If there is none then assign the closest one on the scene.
    for pac in pacs_mine:
        pr("pac: ", pac)
        # Initialize the selected target.
        selected_target = None
        
        # Go to the visible pellets.
        pr("normal pellets", normal_pellets)
        if len(normal_pellets) > 0:
            pr("There are visible normal pellets")
            directions = {'up': {}, 'down': {}, 'left': {}, 'right': {}}

            # Calculate the proximity for all normal pellets.
            for pellet in normal_pellets:
                proximity, direction = calc_pellets_proximity(pac['position'], pellet, scene)
                if proximity >= 0:
                    directions[direction][pellet] = proximity

            # Find the direction that gives the most value per distance (cost).
            max_expected_value = -math.inf
            selected_direction = None
            for direction, targets in directions.items():
                if len(targets) > 0:
                    max_proximity = -math.inf
                    for target, proximity in targets.items():
                        if proximity > max_proximity:
                            max_proximity = proximity
                    # Heuristic calculation of the expected value.
                    value = len(targets)
                    density = value / (max_proximity + 1)
                    expected_value = value * (density**2)
                    if expected_value > max_expected_value:
                        max_expected_value = expected_value
                        selected_direction = direction

            # Find the most distant one from the selected direction.
            if selected_direction:
                selected_target = None
                max_proximity = -math.inf
                for target, proximity in directions[selected_direction].items():
                    if proximity > max_proximity:
                        max_proximity = proximity
                        selected_target = target

            # If the stack exists get it, otherwise create it.
            if pac['id'] in last['pellet_stack']:
                stack = last['pellet_stack'][pac['id']]
            else:
                stack = []

            # The visible pellets from the non selected directions are stored in the stack.
            for direction, targets in directions.items():
                if direction != selected_direction:
                    for target in targets:
                        if target in stack:
                            stack.remove(target)
                        stack.append(target)
            
            # Update the stack
            last['pellet_stack'][pac['id']] = stack

        # Go to the stacked pellets.
        if selected_target is None:
            if pac['id'] in last['pellet_stack']:
                stack = last['pellet_stack'][pac['id']]
                if len(stack) > 0:
                    for target in stack:
                        selected_target = stack.pop()

        # Check if the existing plan should be reused.
        if selected_target is None:
            if last['normal_pellet_plan'] is not None:
                if pac['id'] in last['normal_pellet_plan']:
                    planned_position = last['normal_pellet_plan'][pac['id']]
                    current_position = pac['position']
                    if current_position != planned_position:
                        selected_target = planned_position
                        pr("NORMAL - USE LAST: ", selected_target)
        

        # Create a new plan
        if selected_target is None:
            # Initialize the poi
            selected_poi = None

            # Calculate the % left of each floor category.
            floor_4_left_percentage = round(len(scene['un_floor_4']) / len(scene['floor_4']), 1)
            floor_3_left_percentage = round(len(scene['un_floor_3']) / len(scene['floor_3']), 1)
            floor_2_left_percentage = round(len(scene['un_floor_2_corner']) / len(scene['floor_2_corner']), 1)

            # Select the pois based on the left %.
            pois = None

            pr("floor_4_left_percentage", floor_4_left_percentage)
            pr("FLOOR_4_PERCENTAGE_THRESHOLD", FLOOR_4_PERCENTAGE_THRESHOLD)
            pr("floor_3_left_percentage", floor_3_left_percentage)
            pr("FLOOR_3_PERCENTAGE_THRESHOLD", FLOOR_3_PERCENTAGE_THRESHOLD)
            pr("floor_2_left_percentage", floor_2_left_percentage)
            pr("FLOOR_2_PERCENTAGE_THRESHOLD", FLOOR_2_PERCENTAGE_THRESHOLD)

            if floor_4_left_percentage > FLOOR_4_PERCENTAGE_THRESHOLD:
                pr("Using un_floor_4")
                pois = scene['un_floor_4']
            elif floor_3_left_percentage > FLOOR_3_PERCENTAGE_THRESHOLD:
                pr("Using un_floor_4 and un_floor_3")
                pois = scene['un_floor_4'] | scene['un_floor_3']
            elif floor_2_left_percentage > FLOOR_2_PERCENTAGE_THRESHOLD:
                pr("Using un_floor_4 un_floor_3 un_floor_2_corner")
                pois = scene['un_floor_4'] | scene['un_floor_3'] | scene['un_floor_2_corner']

            dead_ends = scene['un_floor_1']

            if pois:
                # Close visible pois in all directions.
                close_visible_pois = set()
                for direction in ['up', 'down', 'left', 'right']:
                    temp_floor = pac['position']
                    last_valid_poi = None
                    for _ in range(MAX_LOOP_TRIES):
                        # TODO debug here.
                        neighbor = get_neighbors(temp_floor, direction)
                        if neighbor in scene['wall']:
                            break
                        if neighbor in pois:
                            last_valid_poi = neighbor
                        temp_floor = neighbor
                    if last_valid_poi is not None:
                        close_visible_pois.add(last_valid_poi)

                # From the close visible pois, select the closest one.
                if close_visible_pois:
                    min_distance = math.inf
                    for poi in close_visible_pois:
                        distance = calc_distance(poi, pac['position'], scene)
                        if distance < min_distance:
                            min_distance = distance
                            selected_poi = poi
                    
                    if selected_poi is None:
                        pr("NORMAL - NEW PLAN - No selected poi in close_visible_pois")
                    else:
                        pr("NORMAL - NEW PLAN - VISIBLE POI", selected_poi)    
                    pr("Visible pois: ", close_visible_pois)
                
                # There is no visible poi, then go to the closest invisible poi. 
                else:
                    min_distance = math.inf
                    for poi in pois:
                        distance = calc_distance(poi, pac['position'], scene)
                        if distance < min_distance:
                            min_distance = distance
                            selected_poi = poi
                    if selected_poi is None:
                        pr("NORMAL - NEW PLAN - No selected poi in ELSE close_visible_pois")
                    else:
                        pr("NORMAL - NEW PLAN - INVISIBLE POI", selected_poi)    

                # The next pac should not select the same poi.
                selected_target = selected_poi
                pois.remove(selected_poi)
        
            elif dead_ends:
                # Move to the closest dead end.
                min_distance = math.inf
                selected_dead_end = None
                for dead_end in dead_ends:
                    distance = calc_distance(dead_end, pac['position'], scene)
                    if distance < min_distance:
                        min_distance = distance
                        selected_dead_end = dead_end
                if selected_poi is not None:
                    pr("NORMAL - NEW PLAN - No selected dead end")

                # The next pac shoudl not select the same dead end.
                selected_target = selected_dead_end
                dead_ends.remove(selected_dead_end)
                pr("NORMAL - NEW PLAN - DEAD-END: ", selected_target)
            else:
                pr("NORMAL - !!! RANDOM !!! RANDOM !!! RANDOM !!!")
                selected_target = random.choice(list(scene['un_floor']))

        # Assign the target to the pac.   
        pac_targets[pac['id']] = selected_target

    return pac_targets


def find_escape_floor(pac_mine, pac_their, scene):
    """
    Find an escape floor which will save our pac from being eaten.
    """

    # Shortcuts
    escapes = scene['escape']
    my_x = pac_mine['position'][0]
    my_y = pac_mine['position'][1]
    their_x = pac_their['position'][0]
    their_y = pac_their['position'][1]

    # Identify the arrangement of the pacs to select the correct escape floor.
    dx = abs(my_x - their_x)
    dy = abs(my_y - their_y)

    # The x is prefered because the width is greater than the height.
    if dx >= dy:
        # Horizontal or diagonal with equal distance on x and y.
        if my_x > their_x:
            return escapes['right']
        else:
            return escapes['left']
    else:
        # Vertical.
        if my_y > their_y:
            return escapes['down']
        else:
            return escapes['up']


def merge_targets(pac_to_super, pac_to_unstuck, pac_to_normal):
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

    return pac_targets


def add_command(command, pac_id, arg=None):
    """
    Create a commend string according to the game protocol
    """

    assert command in ["MOVE", "SPEED", "SWITCH"]

    if command == "MOVE":
        target = arg
        COMMANDS.append(f"MOVE {pac_id} {target[0]} {target[1]} ({target[0]},{target[1]})")

    elif command == "SPEED":
        COMMANDS.append(f"SPEED {pac_id} SPEED")

    elif command == "SWITCH":
        pac_their_type = arg
        switch_to_type = advice_rps(pac_their_type)

        pr("their type", pac_their_type)
        pr("advice", switch_to_type)

        COMMANDS.append(f"SWITCH {pac_id} {switch_to_type} {switch_to_type}")


def execute_commands(pacs, pac_targets, last, scene):
    """
    Generate and execute the commands.
    """

    # Calculate game maturity
    game_maturity = round(1 - (len(scene['un_floor']) / len(scene['floor'])), 1)
    pr("game_maturity", game_maturity)
    pr("visible enemies", pacs['their'])

    for pac_mine in pacs['mine']:
        pr(" ")
        pr("pac", pac_mine)

        # Check if there is any visible enemies to count piece turns.
        peace_turn = True
        min_proximity = math.inf
        for pac_their in pacs['their']:
            proximity = calc_pacs_proximity(pac_mine['position'], pac_their['position'], pacs, scene)
            if proximity >= 0:
                peace_turn = False
                break
        
        if peace_turn:
            if pac_mine['id'] in last['peace_turns']:
                last['peace_turns'][pac_mine['id']] += 1
                pr("last['peace_turns'][pac_mine['id']]", last['peace_turns'][pac_mine['id']])
            else:
                last['peace_turns'][pac_mine['id']] = 0
                pr("last['peace_turns'][pac_mine['id']]", last['peace_turns'][pac_mine['id']])
        else:
            last['peace_turns'][pac_mine['id']] = 0
            pr("last['peace_turns'][pac_mine['id']]", last['peace_turns'][pac_mine['id']])
        
        # Find the closest compatible enemy to hunt (SPEED / MOVE).
        min_proximity = math.inf
        selected_enemy = None
        for pac_their in pacs['their']:
            proximity = calc_pacs_proximity(pac_mine['position'], pac_their['position'], pacs, scene)
            if proximity >= 0 and proximity <= MAX_PROXIMITY_TO_HUNT:
                win_rps = play_rps(pac_mine['type_id'], pac_their['type_id']) == 1
                if win_rps:
                    pr("we WIN in rps")
                    if proximity < min_proximity:
                        min_proximity = proximity
                        selected_enemy = pac_their
        if selected_enemy is not None:
            lost_rps = play_rps(pac_mine['type_id'], selected_enemy) == -1
            # #if (proximity == 0 and pac_their['ability_cooldown'] <= 1) or (proximity == 0 and lost_rps):
            if (proximity == 0 and pac_their['ability_cooldown'] == 1) or (proximity == 0 and lost_rps):
                escape_floor = find_escape_floor(pac_mine, pac_their, scene)
                pr("MOVE AWAY. The proximity is 0 but the enemy ability cooldown 1", escape_floor)
                pr("Enemy to move away selected", selected_enemy)
                pr("min_proximity", min_proximity)
                pr("pac_mine['position']", pac_mine['position'])
                pr("selected_enemy['position']", selected_enemy['position'])
                pr("pac_mine['type_id']", pac_mine['type_id'])
                pr("selected_enemy['type_id']", selected_enemy['type_id'])
                add_command("MOVE", pac_mine['id'], escape_floor)
                continue

            # # elif (proximity == 0 and pac_their['ability_cooldown'] > 1) or (proximity > 0 and pac_mine['ability_cooldown'] <= pac_their['ability_cooldown']):
            elif (proximity == 0 and pac_their['ability_cooldown'] > 1) or (proximity > 0 and pac_mine['ability_cooldown'] > 0):

                pr("closest COMPATIBLE enemy selected", selected_enemy)
                pr("min_proximity", min_proximity)
                pr("pac_mine['position']", pac_mine['position'])
                pr("selected_enemy['position']", selected_enemy['position'])
                pr("pac_mine['type_id']", pac_mine['type_id'])
                pr("selected_enemy['type_id']", selected_enemy['type_id'])
                pr("ATTACK since it is FACE TO FACE", selected_enemy['position'])
                add_command("MOVE", pac_mine['id'], selected_enemy['position'])
                continue
            else:
                pr("closest COMPATIBLE enemy selected", selected_enemy)
                pr("min_proximity", min_proximity)
                pr("pac_mine['position']", pac_mine['position'])
                pr("selected_enemy['position']", selected_enemy['position'])
                pr("pac_mine['type_id']", pac_mine['type_id'])
                pr("selected_enemy['type_id']", selected_enemy['type_id'])
                pr("SPEED since it is NOT face to face", selected_enemy['position'])
                add_command("SPEED", pac_mine['id'])
                continue
        else:
            pr("No compatible enemy to hunt")

        # Find the closest incompatible enemy to switch against it.
        min_proximity = math.inf
        selected_enemy = None
        for pac_their in pacs['their']:
            proximity = calc_pacs_proximity(pac_mine['position'], pac_their['position'], pacs, scene)
            if proximity >= 0 and proximity <= MAX_PROXIMITY_TO_HUNT:
                win_rps = play_rps(pac_mine['type_id'], pac_their['type_id']) == 1
                if not win_rps:
                    pr("we DONT WIN in rps")
                    if proximity < min_proximity:
                        min_proximity = proximity
                        selected_enemy = pac_their
        if selected_enemy is not None and pac_mine['ability_cooldown'] == 0:
            pr("closest INCOMPATIBLE enemy selected", selected_enemy)
            pr("min_proximity", min_proximity)
            pr("pac_mine['position']", pac_mine['position'])
            pr("selected_enemy['position']", selected_enemy['position'])
            pr("pac_mine['type_id']", pac_mine['type_id'])
            pr("selected_enemy['type_id']", selected_enemy['type_id'])
            pr("SWITCH as we are incompatible", selected_enemy['position'])
            add_command("SWITCH", pac_mine['id'], pac_their['type_id'])
            continue
        else:
            pr("No incompatible enemy to switch against")

        pr("No aggressive actions can be taken")

        if game_maturity < GAME_MATURITY_FOR_SPEEDS:
            pr("SPEED abuse as maturity is low", game_maturity)
            add_command("SPEED", pac_mine['id'])
            continue
        
        if pac_mine['id'] in last['peace_turns']:
            if last['peace_turns'][pac_mine['id']] > MIN_PEACE_TO_SPEED:
                if pac_mine['speed_turns_left'] == 0 and pac_mine['ability_cooldown'] == 0:
                    pr("SPEED as too many turns in peace", last['peace_turns'])
                    add_command("SPEED", pac_mine['id'])
                    continue

        if True:
            pr("pac_mine['id']", pac_mine['id'])
            pr("pac targets", pac_targets)
            pr("MOVE to target", pac_targets[pac_mine['id']])
            add_command("MOVE", pac_mine['id'], pac_targets[pac_mine['id']])
            continue

    # Execute the commands
    print("  |  ".join(COMMANDS))


def main():

    # Read the scene.
    scene = read_scene()

    # Initialize the cross turn variables.
    last = {
        'super_pellet_count': -1, 
        'super_pellet_plan': None,
        'normal_pellet_plan': None,
        'pacs_mine': {},
        'pellet_stack': {},
        'peace_turns': {}}

    # Game loop.
    turn = 0
    while True:
        # Reset commands
        global COMMANDS 
        COMMANDS = []

        # Read score.
        score = {}
        score['mine'], score['their'] = [int(i) for i in input().split()]

        # Read pacs.
        pacs = read_pacs()

        # for pac in pacs['mine']:
        #     pr("pac mine", pac)
        # for pac in pacs['their']:
        #     pr("pac their", pac)

        # Update the unexplored floor.
        scene = update_unexplored(scene, pacs)

        # Read pellets.
        pellet_count, super_pellets, normal_pellets = read_pellets()

        # Pass 1 - Resolve stucks
        available_pacs = find_available_pacs(pacs)
        pac_to_unstuck = resolve_stucks(available_pacs, last, scene)

        # Pass 2 - Collect super pellets
        available_pacs = find_available_pacs(pacs, pac_to_unstuck)
        pac_to_super = collect_super_pellets(available_pacs, super_pellets, last, scene)

        # Pass 3 - Collect normal pellets.
        available_pacs = find_available_pacs(pacs, pac_to_unstuck, pac_to_super)
        pac_to_normal = collect_normal_pellets(available_pacs, normal_pellets, last, scene)

        # Merge the pac targets.
        pac_targets = merge_targets(pac_to_super, pac_to_unstuck, pac_to_normal)
        pr("pac to super"  , pac_to_super)
        pr("pac to unstack", pac_to_unstuck)
        pr("pac to normal" , pac_to_normal)
        pr("pac targets", pac_targets)
        
        # Generate and execute the commands
        execute_commands(pacs, pac_targets, last, scene)
        
        # Update the cross turn variables.
        last['super_pellet_count'] = len(super_pellets)
        last['super_pellet_plan'] = pac_to_super
        last['normal_pellet_plan'] = pac_to_normal
        last['pacs_mine'] = copy.deepcopy(pacs['mine'])

        # Update the turn
        turn += 1        

# Entry point.
main()