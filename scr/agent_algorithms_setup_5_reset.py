#pass
from voxel_builder_library import pheromon_loop, make_solid_box_z, make_solid_box_xxyyzz
from class_agent import Agent
from class_layer import Layer
# from voxel_builder_library import get_chance_by_climb_style, get_chance_by_relative_position, get_chances_by_density
import numpy as np

"""
SETUP GOAL
testing pheromon method
"""

# overal settings
voxel_size = 40
agent_count = 1
wait_to_diffuse = 0

# BUILD OVERALL SETTINGS
reach_to_build = 6
reach_to_erase = 2
stacked_chances = True
reset_after_build = False

# make boundary
# global margin_ratio, fly
fly = False

# MOVE PRESETS - pheromon layers
move_ph_random_strength = 0.1
move_ph_queen_bee = 1
move_ph_sky = 0
move_ph_moisture = 0

# direction preference
move_dir_prefer_to_side = 1
move_dir_prefer_to_up = 1
move_dir_prefer_to_down = 3
move_dir_prefer_strength = 0

# queen bee:
queens_place = [30,0,2]
queens_place_array = np.zeros([voxel_size, voxel_size, voxel_size])
x,y,z = queens_place
queens_place_array[x][y][z] = 1

check_collision = False
keep_in_bounds = True
# if not keep in bounds, agents reset if out of bounds

# global ground_level_Z, enter_zone_a, enter_zone_b
ground_level_Z = 1
enter_zone_a = 25
enter_zone_b = 28

solid_box = None
solid_box = [25,26,0,30,ground_level_Z,12]
# solid_box = [10,20,10,20,0,6]
# solid_box = [0,1,0,1,0,1]

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
    rgb_queen = [232, 226, 211]
    rgb_queen = [237, 190, 71]



    ground = Layer(voxel_size=voxel_size, name='ground', rgb = [i/255 for i in rgb_ground])
    agent_space = Layer('agent_space', voxel_size = voxel_size, rgb = [i/255 for i in rgb_agents])
    # queen_bee_space = Layer(voxel_size=voxel_size, rgb=[203/255, 21/255, 207/255])
    queen_bee_pheromon = Layer('queen_bee_pheromon', voxel_size=voxel_size, rgb = [i/255 for i in rgb_queen], flip_colors = True)
    clay_moisture_layer = Layer('clay_moisture', voxel_size, rgb = [i/255 for i in rgb_clay_moisture], flip_colors=True)
    air_moisture_layer = Layer('air_moisture', voxel_size, rgb = [i/255 for i in rgb_air_moisture], flip_colors=True)

    queen_bee_pheromon.diffusion_ratio = 1/7
    queen_bee_pheromon.decay_ratio = 0.001
    queen_bee_pheromon.gradient_resolution = 0

    ground.decay_linear_value = 1 / iterations / 10
    clay_moisture_layer.decay_linear_value = 1 / iterations / agent_count / 2
    # print(clay_moisture_layer.decay_linear_value)
    # print(ground.decay_linear_value)

    air_moisture_layer.diffusion_ratio = 1/12
    air_moisture_layer.decay_ratio = 1/4
    air_moisture_layer.gradient_resolution = 100000

    ### CREATE GROUND
    # make ground
    
    # ground.array += make_solid_box_z(voxel_size, ground_level_Z)
    ground.array[:,:,:ground_level_Z] = 1
    # print(ground.array)
    if solid_box != None:
        wall = make_solid_box_xxyyzz(voxel_size, *solid_box)
        ground.array += wall
    ground.rgb = [207/255, 179/255, 171/255]

    # set ground moisture
    clay_moisture_layer.array = ground.array.copy()
    # pheromon_loop(air_moisture_layer, clay_moisture_layer.array, 3, ground)
    
    # pheromon_loop(sky_ph_layer, build_boundary_pheromon.array, wait_to_diffuse, blocking_layer=ground, gravity_shift_bool = True)

    # WRAP ENVIRONMENT
    layers = {'agent_space' : agent_space, 'air_moisture_layer' : air_moisture_layer, 'clay_moisture_layer' : clay_moisture_layer, 
              'ground' : ground, 'queen_bee_pheromon' : queen_bee_pheromon}
    settings = {"agent_count" : agent_count, "voxel_size" : voxel_size}
    return settings, layers

def diffuse_environment(layers):
    # air_moisture_layer = layers['air_moisture_layer']
    ground = layers['ground']
    # clay_moisture_layer = layers['clay_moisture_layer']
    queen_bee_pheromon = layers['queen_bee_pheromon']
    # sky_ph_layer = layers['sky_ph_layer']

    # queen_bee_pheromon.emission_intake(external_emission_array = queens_place_array, factor = 1)
    # queen_bee_pheromon.diffuse()
    # queen_bee_pheromon.decay()
    # ground.block_layers([queen_bee_pheromon])
    # queen_bee_pheromon.grade()
    
    pheromon_loop(queen_bee_pheromon, emmission_array=queens_place_array, blocking_layer=ground)
    # pheromon_loop(air_moisture_layer, emmission_array = clay_moisture_layer.array, blocking_layer = ground)
    pass

def setup_agents(layers):
    agent_space = layers['agent_space']
    ground = layers['ground']
    agents = []
    for i in range(agent_count):
        # create object
        agent = Agent(
            space_layer = agent_space, ground_layer = ground,
            track_layer = None, leave_trace=False, save_move_history=True)
        
        # drop in the middle
        reset_agent(agent)

        agents.append(agent)
    return agents

def reset_agent(agent):
    # centered setup
    a, b = [enter_zone_a, enter_zone_b]
    
    x = np.random.randint(a, b)
    y = np.random.randint(a, b)
    # z = np.random.randint(a, b)

    agent.pose = [x,y,ground_level_Z]

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

    # # PRESETS
    # move_ph_random_strength = 1.2
    # move_ph_queen_bee = 0
    # move_ph_moisture = 1

    # move_dir_prefer_to_side = 1
    # move_dir_prefer_to_up = 1
    # move_dir_prefer_to_down = 1
    # move_dir_prefer_strength = 0

    move_ph_strength_list = [
        move_ph_queen_bee,
        move_ph_moisture
    ]

    move_ph_layers_list = [
        layers['queen_bee_pheromon'],
        layers["air_moisture_layer"]
    ]

    move_dir_preferences = [
        move_dir_prefer_to_up,
        move_dir_prefer_to_side,
        move_dir_prefer_to_down
    ]

    pose = agent.pose
    cube = np.random.random(26) * move_ph_random_strength
    for s, layer in zip(move_ph_strength_list, move_ph_layers_list):
        if layer != None:
            # cube = get_sub_array(array = layer.array, offset_radius = 1, center = pose, format_values = None)
            cube += s * agent.get_nb_26_cell_values(layer, pose)
        else: pass

    if move_dir_preferences != None:
        up, side, down = move_dir_preferences
        cube += agent.direction_preference_26_pheromones_v2(up, side, down) * move_dir_prefer_strength
    # moved = agent.move_on_ground(layers['ground'], voxel_size)
    moved = agent.move_on_ground_by_cube(ground=layers['ground'], pheromon_cube=cube, voxel_size=voxel_size, fly = False, only_bounds = keep_in_bounds)
    
    # check if in bounds
    if 0 > np.min(agent.pose) or np.max(agent.pose) >= voxel_size :
        # print(agent.pose)
        moved = False

    return moved

def calculate_build_chances(agent, layers):
    """PLACEHOLDER NOT REMOVED!
    build_chance, erase_chance = [0.2,0]
    function operating with Agent and Layer class objects
    calculates probability of building and erasing voxels 
    combining several density analyses

    returns build_chance, erase_chance
    """
    ground = layers['ground']

    build_chance = agent.build_chance
    erase_chance = agent.erase_chance

    # RELATIVE POSITION
    c = agent.get_chance_by_relative_position(
        ground,
        build_below = 2,
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
            build_if_over = 9,
            build_if_below = 30,
            erase_if_over = 0,
            erase_if_below = 8,
            build_strength = 1)
    build_chance += c
    erase_chance += e

    return build_chance, erase_chance

def build(agent, layers, build_chance, erase_chance, decay_clay = False):
    ground = layers['ground']
    clay_moisture_layer = layers['clay_moisture_layer']
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
            # reset_agent = True
            if decay_clay:
                clay_moisture_layer.decay_linear()
    elif agent.erase_chance >= reach_to_erase and build_condition == True:
        erased = agent.erase(ground)
        erased2 = agent.erase(clay_moisture_layer)
    # else: 
    #     built = False
    #     erased = False
    return built, erased
