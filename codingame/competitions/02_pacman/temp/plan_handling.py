    """
    The planning for each pac is done once and it is updated until it is achieved.
    """
    # There is no plan or super pellets have been captured.
    there_is_no_normal_pellet_plan = last['normal_pellet_plan'] == None

    if there_is_no_normal_pellet_plan:
        print("collect normal pellet - NEW PLAN", file=sys.stderr)
        return plan_normal_pellets(pacs_mine, normal_pellets, scene)
    else:
        print("collect normal pellet - USE LAST", file=sys.stderr)
        return last['normal_pellet_plan']