        targets = normal_pellets

        pac_targets = [None] * len(pacs_mine)
        for p, pac in enumerate(pacs_mine):
            if pac_targets[p] is None:
                min_distance = math.inf
                closest_target = None
                for target in targets:
                    distance = calc_distance(pac["position"], target)
                    if distance < min_distance:
                        min_distance = distance
                        closest_target = target