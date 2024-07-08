#pass

def build_by_last_move(
        agent, 
        climb = 0.5,
        top = 2,
        walk = 0.1,
        descend = -0.05,
        build_strength__last_move = 0):
    pass

def build_by_relative_position(
        agent,
        build_below = -1,
        build_aside = -1,
        build_above = 1,
        build_strength = 1):
    pass

def build_in_density(
        agent, 
        layer,
        radius,
        build_if_over = 20,
        build_if_below = 5,
        build_strength = 1):
    pass

def build_or_erase_by_density(
        agent, 
        layer,
        radius,        
        build_if_over = 0,
        build_if_below = 5,
        erase_if_over = 20,
        erase_if_below = 27,
        build_strength = 1):
    pass