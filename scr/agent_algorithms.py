#pass

# generative behaviours can be stored in these 'algorithm' files, and called from main
# as preset_variables and preset_functions


def build_by_chance(agent, ground, queen_bee_pheromon, air_moisture_layer, sky_ph_layer):
    # build by last move settings
    climb = 0.5
    top = 2
    walk = 0.1
    descend = -0.05
    build_strength__last_move = 0

    # build by relative position
    build_below = -1
    build_aside = -1
    build_above = 1
    build_strength__relative_position = 0

    # build or destroy by built_density
    # NOTE this could be directional scanning perhaps
    erase_if_below__built_density = 27
    erase_if_over__built_density = 20
    build_if_below__built_density = 5
    build_if_over__built_density = 0
    density_scan_radius__built_density = 1
    build_strength__built_density = 0

    # build_in_density -- queen bee ph
    build_if_over__queen_bee = 0.005
    build_if_below__queen_bee = 0.05
    build_strength__queen_bee_ph = 0
    density_scan_radius__queen_bee_ph = 0

    # build_in_density -- air moisture
    build_if_over__air_moisture = 0.005
    build_if_below__air_moisture = 0.05
    build_strength__air_moisture = 0
    density_scan_radiues__air_moisture = 0

    # build_in_density -- sky ph
    build_if_over__sky_ph = 0.005
    build_if_below__sky_ph = 0.05
    build_strength__sky_ph = 0
    density_scan_radius__sky_ph = 0

    build_by_last_move(
        agent, 
        climb,
        top,
        walk,
        descend,
        build_strength__last_move)

    build_by_relative_position(
        agent,
        ground,
        build_below,
        build_aside,
        build_above,
        build_strength__relative_position)

    build_or_erase_by_density(
        agent, 
        ground,
        density_scan_radius__built_density,        
        build_if_over__built_density,
        build_if_below__built_density,
        erase_if_over__built_density,
        erase_if_below = 27,
        build_strength = 1)

    build_in_density(
        agent, 
        queen_bee_pheromon,
        density_scan_radius__built_density,
        build_if_over__queen_bee,
        build_if_below__queen_bee,
        build_strength__queen_bee_ph)

    build_in_density(
        agent, 
        air_moisture_layer,
        build_if_over__air_moisture,
        build_if_below__air_moisture,
        build_strength__air_moisture,
        density_scan_radiues__air_moisture)

    build_in_density(
        agent, 
        sky_ph_layer,
        build_if_over__sky_ph,
        build_if_below__sky_ph,
        build_strength__sky_ph,
        density_scan_radius__sky_ph)

    build_chance, erase_chance = [0.2,0]

    return build_chance, erase_chance


    build_condition = agent.check_build_conditions(ground)
    if build_chance >= reach_to_build and build_condition == True:
        done = agent.build()
        if done:
            reset_agent = True
    elif erase_chance >= reach_to_erase and build_condition == True:
        # done = agent.erase()
        # if done:
        #     reset_agent = True
        pass


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
        layer,
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