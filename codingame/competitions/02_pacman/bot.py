import itertools
import sys
import math


SUPER_PELLET_VALUE = 10

def read_scene():
    """
    Reads the scene.
    '#' represents wall
    ' ' represents floor
    The top left corner is the (x=0, y=0)
    """
    width, height = [int(i) for i in input().split()]
    scene_dict = {'width': width, 'height': height, 'rows': []}

    for _ in range(height):
        scene_dict['rows'].append(input())

    return scene_dict


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


def assign_targets(pacs_mine, targets, clusters, width):
    """
    Assign each cluster to the closest pack based on distance.
    """

    assert len(pacs_mine) >= len(clusters)

    pac_to_target = {}

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
        pac_to_target[selected_pac['id']] = selected_target

        # Remove the pac.
        pacs_mine = [x for x in pacs_mine if not (x.get('id') == selected_pac['id'])]

        # Remove the cluster.
        clusters = [x for x in clusters if not x == selected_cluster]

    return pac_to_target


def main():

    # Read the scene.
    scene = read_scene() 

    # Game loop.
    turn = 0
    while True:

        # Read score.
        my_score, opponent_score = [int(i) for i in input().split()]

        # Read pacs.
        pacs_mine, pacs_their = read_pacs()

        # Read pellets.
        pellet_count, super_pellets, normal_pellets = read_pellets()

        # Phase 1 - Super pellets
        if len(super_pellets) > 0:

            # Cluster the super pellets.
            super_pellets_clusters = calc_clusters(super_pellets, len(pacs_mine), scene['width'])

            # Assign a cluster to each pac.
            pac_targets = assign_targets(pacs_mine, super_pellets, super_pellets_clusters, scene['width'])

        # Phase 2 - Normal pellets
        else:
            pass
        
        # Print out the result.
        print(f"pack targets: {pac_targets}", file=sys.stderr)

        # Command generation.
        moves = [f"MOVE {pac} {target[0]} {target[1]}" for pac, target in pac_targets.items()]
        speeds = [f"SPEED {pac['id']}" for pac in pacs_mine]
       
        # Turn handler.
        if turn % 10 == 0:
            print("|".join(speeds))
        else:
            print("|".join(moves))
        turn += 1


# Entry point.
main()