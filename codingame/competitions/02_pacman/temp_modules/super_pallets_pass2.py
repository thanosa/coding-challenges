    # Checks if there are available pacs.
    if len(pacs_mine) > 0:
        print(f"Available pacs: {pacs_mine}", file=sys.stderr)
        for pac in pacs_mine:
            max_distance = -1
            selected_target = None
            for target in unexplored:
                distance = calc_distance(pac['position'], target, width)

                print(f"pac: {pac['id']}", file=sys.stderr)
                print(f"target: {target}", file=sys.stderr)
                print(f"distance: {distance}", file=sys.stderr)
                print(f"min_distance: {min_distance}",file=sys.stderr)
                if distance > max_distance:
                    distance = max_distance
                    selected_target = target
            
            assert selected_target is not None

            # Assign the target to the pac.s
            pac_target[pac['id']] = selected_target