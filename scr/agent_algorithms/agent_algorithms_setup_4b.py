#pass
from voxel_builder_library import pheromon_loop, make_solid_box_z, make_solid_box_xxyyzz
from class_agent import Agent
from class_layer import Layer
# from voxel_builder_library import get_chance_by_climb_style, get_chance_by_relative_position, get_chances_by_density
import numpy as np

"""
DESIGN INTENTION
1. sky ph as attractor volume and build boundary
2. control build by ground density and 


parameter changes
reach to build >> 6
dont reset
"""
# generative behaviours can be stored in these 'algorithm' files, and called from main
# as preset_variables and preset_functions
# MOVE SETTINGS
# move_dir_preference settings w pheromon weights
"""    layers = [agent_space, air_moisture_layer, build_boundary_pheromon, clay_moisture_layer,  ground, queen_bee_pheromon, sky_ph_layer]
"""

# overal settings
voxel_size = 40
agent_count = 15
wait_to_diffuse = 1

ground_edge = 15

# BUILD OVERALL SETTINGS
reach_to_build = 2
reach_to_erase = 2
stacked_chances = True
reset_after_build = True

# move PRESETS
move_ph_random = 0.2
move_ph_queen_bee = 0
move_ph_sky = 1
move_ph_moisture = 0

move_dir_prefer_to_side = 0.5
move_dir_prefer_to_up = 1
move_dir_prefer_to_down = 0
move_dir_prefer_strength = 1

# make boundary
global margin_ratio
margin_ratio = 4
def margin_boundaries(size, parts):
    """return margin start and end integrers"""
    n = parts
    boundary_a = int(1 / n * size)
    boundary_b = int((1 - 1 / n) * size)
    return boundary_a, boundary_b


def layer_env_setup(iterations):
    """
    creates the simulation environment setup
    with preset values in the definition
    
    returns: [settings, layers, clai_moisture_layer]
    layers = [agent_space, air_moisture_layer, build_boundary_pheromon, clay_moisture_layer,  ground, queen_bee_pheromon, sky_ph_layer]
    settings = [agent_count, voxel_size]
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
    wall = make_solid_box_xxyyzz(voxel_size, 20,30,20,30,0,10)
    ground.array += wall
    ground.rgb = [207/255, 179/255, 171/255]

    # set ground moisture
    clay_moisture_layer.array = ground.array.copy()
    pheromon_loop(air_moisture_layer, clay_moisture_layer.array, 3, ground)

    # make boundary
    a, b = margin_boundaries(voxel_size, margin_ratio)

    build_boundary_pheromon = Layer('build_boundary_ph', voxel_size=voxel_size, rgb = [i/255 for i in rgb_sky])
    build_boundary_pheromon.array = np.zeros([voxel_size, voxel_size, voxel_size])
    build_boundary_pheromon.array[a:b][a:b][0:voxel_size - 1] = 1
    
    # pheromon_loop(sky_ph_layer, build_boundary_pheromon.array, wait_to_diffuse, blocking_layer=ground, gravity_shift_bool = True)

    # WRAP ENVIRONMENT
    layers = [agent_space, air_moisture_layer, build_boundary_pheromon, clay_moisture_layer,  ground, queen_bee_pheromon, sky_ph_layer]
    settings = [agent_count, voxel_size]
    return settings, layers, clay_moisture_layer

def diffuse_environment(layers):

    agent_space, air_moisture_layer, build_boundary_pheromon, clay_moisture_layer,  ground, queen_bee_pheromon, sky_ph_layer = layers

    pheromon_loop(sky_ph_layer, emmission_array = build_boundary_pheromon, blocking_layer=ground, gravity_shift_bool = True)
    pheromon_loop(air_moisture_layer, emmission_array = clay_moisture_layer.array, blocking_layer = ground)
    pass

def setup_agents(layers):
    agent_space = layers[0]
    ground = layers[4]
    agents = []
    for i in range(agent_count):
        # create object
        agent = Agent(
            space_layer = agent_space, ground_layer = ground,
            track_layer = None, leave_trace=False, save_move_history=True)
        
        # drop in the middle
        reset_agent(agent, voxel_size)

        agents.append(agent)
    return agents

def reset_agent(agent, voxel_size):
    # centered setup
    a, b = margin_boundaries(voxel_size, margin_ratio + 2)
    
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
    agent_space, air_moisture_layer, build_boundary_pheromon, clay_moisture_layer,  ground, queen_bee_pheromon, sky_ph_layer = layers

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
        up, side, down = move_dir_preferences
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
    ground = layers[4]

    build_chance = agent.build_chance
    erase_chance = agent.erase_chance

    # RELATIVE POSITION
    c = agent.get_chance_by_relative_position(
        ground,
        build_below = 1,
        build_aside = 1,
        build_above = 1,
        build_strength = 0.1)
    build_chance += c

    # surrrounding ground_density
    c, e = agent.get_chances_by_density(
            ground,      
            build_if_over = 8,
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
    ground = layers[4]
    clay_moisture_layer = layers[3]
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
        if built and reset_after_build:
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
