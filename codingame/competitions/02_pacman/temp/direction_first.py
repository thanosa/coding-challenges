    for pac in pacs_mine:
        if pois:
            # These are the targets on the same row or column. Used for performance only.
            # # aligned_un_targets = [t for t in un_targets if t[0] == pac['position'][0] or t[1] == pac['position'][1]]
            
            # Close visible pois in all directions.
            close_visible_pois = set()
            for direction in ['up', 'down', 'left', 'right']:
                temp_floor = pac['position']
                last_valid_poi = None
                while True:
                    neighbor = get_neighbors(temp_floor, direction)
                    if neighbor in scene['wall']:
                        break
                    if neighbor in pois:
                        last_valid_poi = neighbor
                    temp_floor = neighbor
                if last_valid_poi is not None:
                    close_visible_pois.add(last_valid_poi)

            # From the close point we select the furthest one.
            further_visible_poi = None
            if close_visible_pois:
                further_visible_poi = None
                max_distance = -math.inf
                for poi in close_visible_pois:
                    distance = calc_distance(poi, pac['position'], scene)
                    if distance > max_distance:
                        max_distance = distance
                        further_visible_poi = poi

            
            
            # There is no visible poi then go to the closest invisible poi. 
            if not close_visible_pois:
                max_distance = math.inf
                invisible_poi = None
                for poi in pois:
                    distance = calc_distance(poi, pac['position'], scene)
                    if distance < max_distance:
                        max_distance = distance
                        invisible_poi = poi

            assert invisible_poi is not None

            # The next pac should not select the same poi.
            pois.remove(invisible_poi)

        elif dead_ends:
            # Move to the closest dead end.
            dead_ends = scene['un_floor_1']
            max_distance = math.inf
            selected_dead_end = None
            for dead_end in dead_ends:
                distance = calc_distance(dead_end, pac['position'], scene)
                if distance < max_distance:
                    max_distance = distance
                    selected_dead_end = dead_end

            assert selected_dead_end is not None

            dead_ends.remove(selected_dead_end)