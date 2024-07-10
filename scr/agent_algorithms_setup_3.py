#pass
from voxel_builder_library import pheromon_loop, make_solid_box_z
from class_agent import Agent
from class_layer import Layer
# from voxel_builder_library import get_chance_by_climb_style, get_chance_by_relative_position, get_chances_by_density
import numpy as np

"""
DESIGN INTENTION
1. sky ph as attractor volume and build boundary
2. control build by ground density and 
"""
# generative behaviours can be stored in these 'algorithm' files, and called from main
# as preset_variables and preset_functions
# MOVE SETTINGS
# move_dir_preference settings w pheromon weights

queen_bee_pheromon, sky_ph_layer, air_moisture_layer = ['','','']

# overal settings
voxel_size = 40
agent_count = 15
wait_to_diffuse = 1

# BUILD OVERALL SETTINGS
reach_to_build = 5
reach_to_erase = 2
stacked_chances = True
go_home_after_build = True


def layer_env_setup(iterations):
    """
    creates the simulation environment setup
    with preset values in the definition
    
    return
    voxel_size, agent_count, ground, queen_bee_pheromon, sky_ph_layer, sky_emission_layer, clay_moisture_layer, air_moisture_layer, agent_space

    """
    ### LAYERS OF THE ENVIRONMENT
    rgb_sky = [29, 77, 222]
    rgb_agents = [34,116,240]
    rgb_clay_moisture = [167, 217, 213]
    rgb_air_moisture = [200, 204, 219]
    rgb_ground = [207, 179, 171]



    ground = Layer(voxel_size=voxel_size, name='ground', rgb = [i/255 for i in rgb_ground])
    agent_space = Layer('agent_space', voxel_size = voxel_size, rgb = [i/255 for i in rgb_agents])
    # queen_bee_space = Layer(voxel_size=voxel_size, rgb=[203/255, 21/255, 207/255])
    queen_bee_pheromon = Layer('queen_bee_pheromon', voxel_size=voxel_size, rgb = [i/255 for i in rgb_sky])
    sky_ph_layer = Layer('sky_ph_layer', voxel_size=voxel_size, rgb = [i/255 for i in rgb_sky])
    clay_moisture_layer = Layer('clay_moisture', voxel_size, rgb = [i/255 for i in rgb_clay_moisture])
    air_moisture_layer = Layer('air_moisture', voxel_size, rgb = [i/255 for i in rgb_air_moisture])

    sky_ph_layer.diffusion_ratio = 1/6
    sky_ph_layer.decay_ratio = 0.01
    sky_ph_layer.gradient_resolution = 10000
    sky_ph_layer.gravity_dir = 5
    sky_ph_layer.gravity_ratio = 0.8

    ground.decay_linear_value = 1 / iterations / 10
    clay_moisture_layer.decay_linear_value = 1 / iterations / agent_count / 2
    # print(clay_moisture_layer.decay_linear_value)
    # print(ground.decay_linear_value)

    air_moisture_layer.diffusion_ratio = 1/12
    air_moisture_layer.decay_ratio = 1/4
    air_moisture_layer.gradient_resolution = 10000


    ### CREATE ENVIRONMENT
    # make ground
    ground_level_Z = 0
    ground.array = make_solid_box_z(voxel_size, ground_level_Z)
    # wall = make_solid_box_xxyyzz(voxel_size, 20,23,20,23,0,3)
    # ground.array += wall
    ground.rgb = [207/255, 179/255, 171/255]

    # set ground moisture
    clay_moisture_layer.array = ground.array.copy()
    pheromon_loop(air_moisture_layer, clay_moisture_layer.array, 3, ground)

    # make sky
    # sky_ph_layer
    sky_emission_layer = Layer('sky_emmision', voxel_size=voxel_size, rgb = [i/255 for i in rgb_sky])
    sky_emission_layer.array = np.zeros([voxel_size, voxel_size, voxel_size])
    sky_emission_layer.array[:][:][voxel_size - 1] = 1
    pheromon_loop(sky_ph_layer, sky_emission_layer.array, wait_to_diffuse, blocking_layer=ground, gravity_shift_bool = True)

    return voxel_size, agent_count, ground, queen_bee_pheromon, sky_ph_layer, sky_emission_layer, clay_moisture_layer, air_moisture_layer, agent_space


def move_agent(
        agent,        
        queen_bee_pheromon = None,
        sky_ph_layer = None,
        air_moisture_layer = None):
    """move agents in a direction, based on several pheromons weighted in different ratios.
    1. random direction pheromon
    2. queen_bee_pheromon = None : Layer class object,
    3. sky_ph_layer = None : Layer class object,
    4. air_moisture_layer
    5. world direction preference pheromons

    Input:
        agent: Agent class object
        queen_bee_pheromon = None : Layer class object,
        sky_ph_layer = None : Layer class object,
        air_moisture_layer = None : Layer class object,
        None layers are passed
    further parameters are preset in the function

    return True if moved, False if not


    """

    # PRESETS
    move_ph_random = 0.2

    move_ph_queen_bee = 0

    move_ph_sky = 1

    move_ph_moisture = 0

    move_dir_prefer_to_side = 0.5
    move_dir_prefer_to_up = 1
    move_dir_prefer_to_down = -0.2
    move_dir_prefer_strength = 0

    check_collision = False

    move_ph_strength_list = [
        move_ph_queen_bee,
        move_ph_sky,
        move_ph_moisture,
    ]

    move_ph_layers_list = [
        queen_bee_pheromon,
        sky_ph_layer,
        air_moisture_layer
    ]

    move_dir_preferences = [
        move_dir_prefer_to_up,
        move_dir_prefer_to_side,
        move_dir_prefer_to_down
    ]

    pose = agent.pose
    cube = move_ph_random
    for s, layer in zip(move_ph_strength_list, move_ph_layers_list):
        if layer != None:
            # cube = get_sub_array(array = layer.array, offset_radius = 1, center = pose, format_values = None)
            cube += s * agent.get_nb_26_cell_values(layer, pose)
        else: pass

    if move_dir_preferences != None:
        side, up, down = move_dir_preferences
        cube += agent.direction_preference_26_pheromones_v2(up, side, down) * move_dir_prefer_strength

    moved = agent.follow_pheromones(cube, check_collision)
    return moved

def calculate_build_chances(agent, ground, queen_bee_pheromon = None, air_moisture_layer = None, sky_ph_layer = None):
    """PLACEHOLDER NOT REMOVED!
    build_chance, erase_chance = [0.2,0]
    function operating with Agent and Layer class objects
    calculates probability of building and erasing voxels 
    combining several density analyses

    returns build_chance, erase_chance
    """


    # # PLACEHOLDER chance settings
    # """dont forget to delete :D"""
    # build_chance = 0.2
    # erase_chance = 0
    build_chance = agent.build_chance
    erase_chance = agent.erase_chance

    # LAST MOVE CHANCE
    climb = 0.5
    top = 2
    walk = 0.1
    descend = -0.05
    build_strength__last_move = 0

    # RELATIVE POSITION
    build_below = -1
    build_aside = -1
    build_above = 1
    build_strength__relative_position = 0

    # DENSITY OF BUILT SURROUNDING
    # NOTE this could be directional scanning perhaps
    erase_if_below__built_density = 27
    erase_if_over__built_density = 15
    build_if_below__built_density = 10
    build_if_over__built_density = 0
    density_scan_radius__built_density = 1
    build_strength__built_density = 2

    # DENSITY OF QUEEN BEE PHEROMONES
    build_if_over__queen_bee = 0.005
    build_if_below__queen_bee = 0.05
    build_strength__queen_bee_ph = 0
    density_scan_radius__queen_bee_ph = 0

    # DENSITY OF AIR MOISTURE
    build_if_over__air_moisture = 0.005
    build_if_below__air_moisture = 0.05
    build_strength__air_moisture = 0
    density_scan_radius__air_moisture = 0

    # DENSITY OF SKY PH
    build_if_over__sky_ph = 0.005
    build_if_below__sky_ph = 0.05
    build_strength__sky_ph = 0
    density_scan_radius__sky_ph = 0

    c = agent.get_chance_by_climb_style( 
        climb,
        top,
        walk,
        descend,
        build_strength__last_move)
    build_chance += c

    c = agent.get_chance_by_relative_position(
        ground,
        build_below,
        build_aside,
        build_above,
        build_strength__relative_position)
    build_chance += c

    # ground surrrounding
    c, e = agent.get_chances_by_density( 
        ground,
        density_scan_radius__built_density,        
        build_if_over__built_density,
        build_if_below__built_density,
        erase_if_over__built_density,
        erase_if_below__built_density,
        build_strength = build_strength__built_density)
    build_chance += c
    erase_chance += e

    # queen bee
    c, e = agent.get_chances_by_density(
        queen_bee_pheromon,
        density_scan_radius__queen_bee_ph,
        build_if_over__queen_bee,
        build_if_below__queen_bee,
        build_strength__queen_bee_ph)
    build_chance += c
    erase_chance += e

    # air_moisture
    c, e = agent.get_chances_by_density(
        air_moisture_layer,
        density_scan_radius__air_moisture,
        build_if_over__air_moisture,
        build_if_below__air_moisture,
        build_strength__air_moisture,
        )
    build_chance += c
    erase_chance += e

    # sky_density
    c, e = agent.get_chances_by_density( 
        sky_ph_layer,
        build_if_over__sky_ph,
        build_if_below__sky_ph,
        build_strength__sky_ph,
        density_scan_radius__sky_ph)
    build_chance += c
    erase_chance += e

    return build_chance, erase_chance

def build(agent, build_chance, erase_chance, ground, clay_moisture_layer, decay_clay = False):
    """agent builds on construction_layer, if pheromon value in cell hits limit
    chances are either momentary values or stacked by history
    return bool"""
    if stacked_chances:
        # print(erase_chance)
        agent.build_chance += build_chance
        agent.erase_chance += erase_chance
    else:
        agent.build_chance = build_chance
        agent.erase_chance = erase_chance

    # CHECK IF BUILD CONDITIONS are favorable
    built = False
    erased = False
    build_condition = agent.check_build_conditions(ground)
    if agent.build_chance >= reach_to_build and build_condition == True:
        built = agent.build(ground)
        built2 = agent.build(clay_moisture_layer)
        if built and go_home_after_build:
            reset_agent = True
            if decay_clay:
                clay_moisture_layer.decay_linear()
    elif agent.erase_chance >= reach_to_erase and build_condition == True:
        erased = agent.erase(ground)
        erased2 = agent.erase(clay_moisture_layer)
    # else: 
    #     built = False
    #     erased = False
    return built, erased

def reset_agent(agent, voxel_size):
    x = np.random.randint(0, voxel_size)
    y = np.random.randint(0, voxel_size)
    agent.pose = [x,y,1]
    agent.build_chance = 0
    agent.erase_chance = 0
    agent.move_history = []
