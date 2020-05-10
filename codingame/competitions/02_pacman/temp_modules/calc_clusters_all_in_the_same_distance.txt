def calc_clusters(targets, pac_count, width):
    """
    The number of clusters should as much as the pacs.
    """
    # Calculate the super pellet to super pellet distances.
    distances_set, distances_dict = calc_s2s_distances(targets, width)
    print(distances_set, distances_dict, file=sys.stderr)

    cluster_count = len(targets)

    # Create clusters
    clusters = []

    while cluster_count > pac_count:
        min_distance = distances_set.pop()

        print(f"min distance: {min_distance}", file=sys.stderr)
        pairs = [entities for entities, distance in distances_dict.items() if distance == min_distance]
        cluster = set([item for sublist in pairs for item in sublist])

        clusters.append(cluster)
        print(f"cluster: {cluster}", file=sys.stderr)

        cluster_count = len(clusters)