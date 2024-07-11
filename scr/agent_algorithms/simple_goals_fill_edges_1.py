#pass
from voxel_builder_library import pheromon_loop, make_solid_box_z
from class_agent import Agent
from class_layer import Layer
# from voxel_builder_library import get_chance_by_climb_style, get_chance_by_relative_position, get_chances_by_density
import numpy as np

"""
DESIGN INTENTION

fill up the edges

"""

# overal settings
voxel_size = 40
agent_count = 15
wait_to_diffuse = 1

# setup variables
enter_corner_width = 8

# BUILD OVERALL SETTINGS
reach_to_build = 1
reach_to_erase = 1
stacked_chances = False
reset_after_build = True


""" ENVIRONMENT:
layers = [agent_space, air_layer, clay_layer,  ground_layer]
settings = [agent_count, voxel_size]

agent_space, air_layer, clay_layer,  ground_layer = layers
agent_count, voxel_size : settings
"""

def layer_env_setup(iterations):
    """
    creates the simulation environment setup
    with preset values in the definition
    
    returns: [settings, layers, clai_moisture_layer]
    layers = [agent_space, air_layer, build_boundary_pheromon, clay_layer,  ground_layer, queen_bee_pheromon, sky_ph_layer]
    settings = [agent_count, voxel_size]
    """
    ### LAYERS OF THE ENVIRONMENT
    rgb_sky = [29, 77, 222]
    rgb_agents = [34,116,240]
    rgb_clay = [167, 217, 213]
    rgb_air = [200, 204, 219]
    rgb_ground_layer = [207, 179, 171]

    ground_layer = Layer(voxel_size=voxel_size, name='ground_layer', rgb = [i/255 for i in rgb_ground_layer])
    agent_space = Layer('agent_space', voxel_size = voxel_size, rgb = [i/255 for i in rgb_agents])
    clay_layer = Layer('clay_layer', voxel_size, rgb = [i/255 for i in rgb_clay])
    air_layer = Layer('air_layer', voxel_size, rgb = [i/255 for i in rgb_air])

    clay_layer.decay_linear_value = 1 / iterations / agent_count / 2

    air_layer.diffusion_ratio = 1/7
    air_layer.decay_ratio = 1/2
    air_layer.gradient_resolution = 100


    ### CREATE ENVIRONMENT
    # make ground_layer
    ground_layer_level_Z = 0
    ground_layer.array = make_solid_box_z(voxel_size, ground_layer_level_Z)
    # wall = make_solid_box_xxyyzz(voxel_size, 20,23,20,23,0,3)
    # ground_layer.array += wall
    ground_layer.rgb = [207/255, 179/255, 171/255]

    # set ground_layer moisture
    clay_layer.array = ground_layer.array.copy()
    pheromon_loop(air_layer, emmission_array = clay_layer.array,i = 3, blocking_layer = ground_layer)
    
    # WRAP ENVIRONMENT
    layers = [agent_space, air_layer, clay_layer, ground_layer]
    settings = [agent_count, voxel_size]
    return settings, layers, clay_layer

"""DIFFUSION:
clay layer decays (dries)
clay layer emits pheromons into the air layer"""

def diffuse_environment(layers):
    """clay layer decays (dries)
    clay layer emits pheromons into the air layer"""
    agent_space, air_layer, clay_layer,  ground_layer = layers
    clay_layer.decay_linear()

    pheromon_loop(air_layer, emmission_array = clay_layer.array, blocking_layer = ground_layer)
    pass

"""Setup:
enter from the bottom_left corner
corner size = enter_corner_width
"""
def setup_agents(layers):
    agent_space = layers[0]
    ground_layer = layers[-1]
    agents = []
    for i in range(agent_count):
        # create object
        agent = Agent(
            space_layer = agent_space, 
            ground_layer = ground_layer,
            save_move_history=True)
        # drop in the corner
        reset_agent(agent, voxel_size)

        agents.append(agent)
    return agents

def reset_agent(agent, voxel_size):
    # centered setup
    a, b = margin_boundaries(voxel_size, margin_ratio + 2)
    a, b = 0, 5
    x = np.random.randint(a, b)
    y = np.random.randint(a, b)
    agent.pose = [x,y,1]

    agent.build_chance = 0
    agent.erase_chance = 0
    agent.move_history = []


def move_agent(agent, layers):
    """move agents in a direction, based on several pheromons weighted in different ratios.
    1. random direction pheromon
    2. queen_bee_pheromon = None : Layer class object,
    3. sky_ph_layer = None : Layer class object,
    4. air_layer
    5. world direction preference pheromons

    Input:
        agent: Agent class object
        queen_bee_pheromon = None : Layer class object,
        sky_ph_layer = None : Layer class object,
        air_layer = None : Layer class object,
        None layers are passed
    further parameters are preset in the function

    return True if moved, False if not


    """
    agent_space, air_layer, build_boundary_pheromon, clay_layer,  ground_layer, queen_bee_pheromon, sky_ph_layer = layers

    # PRESETS
    move_ph_random = 0.2

    move_ph_queen_bee = 0

    move_ph_sky = 1

    move_ph_moisture = 0

    move_dir_prefer_to_side = 0.5
    move_dir_prefer_to_up = 1
    move_dir_prefer_to_down = 1
    move_dir_prefer_strength = 3

    check_collision = False

    move_ph_strength_list = [
        move_ph_queen_bee,
        move_ph_sky,
        move_ph_moisture,
    ]

    move_ph_layers_list = [
        queen_bee_pheromon,
        sky_ph_layer,
        air_layer
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

def calculate_build_chances(agent, layers):
    """PLACEHOLDER NOT REMOVED!
    build_chance, erase_chance = [0.2,0]
    function operating with Agent and Layer class objects
    calculates probability of building and erasing voxels 
    combining several density analyses

    returns build_chance, erase_chance
    """

    boundary = layers[2]
    ground_layer = layers[4]

    build_chance = agent.build_chance
    erase_chance = agent.erase_chance

    # RELATIVE POSITION
    c = agent.get_chance_by_relative_position(
        ground_layer,
        build_below = 2,
        build_aside = 1,
        build_above = 1,
        build_strength = 0.1)
    build_chance += c

    # surrrounding ground_layer_density
    c, e = agent.get_chances_by_density(
            ground_layer,      
            build_if_over = 0,
            build_if_below = 15,
            erase_if_over = 21,
            erase_if_below = 30,
            build_strength = 1)
    build_chance += c
    erase_chance += e

    # boundary
    c, e = agent.get_chances_by_density(
            boundary,      
            build_if_over = 9,
            build_if_below = 30,
            erase_if_over = 0,
            erase_if_below = 8,
            build_strength = 1)
    build_chance += c
    erase_chance += e

    return build_chance, erase_chance

def build(agent, layers, build_chance, erase_chance, decay_clay = False):
    ground_layer = layers[4]
    clay_layer = layers[3]
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
    build_condition = agent.check_build_conditions(ground_layer)
    if agent.build_chance >= reach_to_build and build_condition == True:
        built = agent.build(ground_layer)
        built2 = agent.build(clay_layer)
        if built and reset_after_build:
            reset_agent = True
            if decay_clay:
                clay_layer.decay_linear()
    elif agent.erase_chance >= reach_to_erase and build_condition == True:
        erased = agent.erase(ground_layer)
        erased2 = agent.erase(clay_layer)
    # else: 
    #     built = False
    #     erased = False
    return built, erased
