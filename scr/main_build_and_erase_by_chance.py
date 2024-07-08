from voxel_builder_library import *
from show_voxel_plt import *
from agent_algorithms import *
from helpers import *
from show_voxel_plt import timestamp_now
from matplotlib import animation
save_animation = False

voxel_size = 60
agent_count = 10
iterations = 2
save_ = False
save_json = False
title_ = 'img'
note = 'build_by_chance_a%s_i%s' %(agent_count, iterations)
time__ = timestamp_now

# global sky_ph_layer, ground, agents

### LAYERS OF THE ENVIRONMENT
rgb_sky = [29, 77, 222]
rgb_agents = [34,116,240]
rgb_clay_moisture = [167, 217, 213]
rgb_air_moisture = [200, 204, 219]
rgb_ground = [207, 179, 171]
wait_to_diffuse = 10

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

clay_moisture_layer.diffusion_ratio = 0
clay_moisture_layer.decay_ratio = 1/24
clay_moisture_layer.gradient_resolution = 0

air_moisture_layer.diffusion_ratio = 1/12
air_moisture_layer.decay_ratio = 1/4
air_moisture_layer.gradient_resolution = 10000

# MOVE SETTINGS
# move_preference settings w pheromon weights

move_ph_random = 0.2
move_ph_queen_bee = 0
move_ph_sky = 1
move_ph_moisture = 0.2
move_prefer_to_side = 0.5
move_prefer_to_up = 1
move_prefer_to_down = -0.2
move_pref_strength = 0.1

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
    move_prefer_to_up,
    move_prefer_to_side,
    move_prefer_to_down
]

def move_agent(
        agent, 
        move_ph_random,
        move_ph_strength_list,
        move_ph_layers_list,
        move_dir_preferences = None, 
        move_pref_strength = 0):

    pose = agent.pose
    cube = move_ph_random
    for s, layer in zip(move_ph_strength_list, move_ph_layers_list):
        # cube = get_sub_array(array = layer.array, offset_radius = 1, center = pose, format_values = None)
        cube += s * agent.get_nb_26_cell_values(layer, pose)

    if move_dir_preferences != None:
        side, up, down = move_dir_preferences
        cube += agent.direction_preference_26_pheromones_v2(up, side, down) * move_pref_strength

    moved = agent.follow_pheromones(cube, check_collision = False)
    return moved
    

# BUILD SETTINGS
construction_on = True
reach_to_build = 2
reach_to_erase = 0.5
stacked_chances = True

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

# make agents
agents = []
for i in range(agent_count):
    agent = Agent(
        space_layer = agent_space, ground_layer = ground, construction_layer = ground,
        track_layer = None, leave_trace=False, save_move_history=True)
    x = np.random.randint(0, voxel_size)
    y = np.random.randint(0, voxel_size)
    agent.pose = [x,y,1]
    agents.append(agent)

def pheromon_loop(pheromon_layer, emmission_array = None, i = 1, blocking_layer = None, gravity_direction = None, gravity_shift_bool = False):
    """gravity direction: 0:left, 1:right, 2:front, 3:back, 4:down, 5:up"""
    for i in range(i):
        # emmission in
        if not isinstance(emmission_array, bool):
            pheromon_layer.emission_intake(emmission_array, 2, False)

        # diffuse
        pheromon_layer.diffuse()

        # gravity
        if gravity_shift_bool:
            pheromon_layer.gravity_shift()

        # decay
        pheromon_layer.decay()

        # collision
        if blocking_layer != None:
            blocking_layer.block_layers([pheromon_layer])
        
        # apply gradient steps
        if pheromon_layer.gradient_resolution != 0:
            pheromon_layer.grade()

### CREATE ENVIRONMENT
# make ground
ground_level_Z = 0
ground.array = make_solid_box_z(voxel_size, ground_level_Z)
# wall = make_solid_box_xxyyzz(voxel_size, 20,23,20,23,0,3)
# ground.array += wall
ground.rgb = [207/255, 179/255, 171/255]

# set ground moisture
clay_moisture_layer.array = ground.array.copy()
print(clay_moisture_layer.array)
pheromon_loop(clay_moisture_layer, None, 3)
pheromon_loop(air_moisture_layer, clay_moisture_layer.array, 3, ground)

# make sky
# sky_ph_layer
sky_emission = np.zeros([voxel_size, voxel_size, voxel_size])
sky_emission[:][:][voxel_size - 1] = 1
pheromon_loop(sky_ph_layer, sky_emission, wait_to_diffuse, blocking_layer=ground, gravity_shift_bool = True)

#  RUN SIMULATION
def iterate(frame):
# for i in range(iterations):
    print(iterate.counter)

    # 1. diffuse environment's layers
    pheromon_loop(sky_ph_layer, emmission_array = sky_emission, blocking_layer=ground, gravity_shift_bool = True)
    pheromon_loop(clay_moisture_layer)
    pheromon_loop(air_moisture_layer, emmission_array = clay_moisture_layer.array, blocking_layer = ground)

    # 2. MOVE and BUILD
    for agent in agents:
        reset_agent = False
        # move
        moved = move_agent(agent, move_ph_random, move_ph_strength_list, move_ph_layers_list, move_dir_preferences, move_pref_strength)
        # build
        if moved and construction_on:
            build_chance, erase_chance = build_by_chance(agent, ground, queen_bee_pheromon, air_moisture_layer, sky_ph_layer)
            if stacked_chances:
                agent.build_chance += build_chance
                agent.erase_chance += erase_chance
            else:
                agent.build_chance = build_chance
                agent.erase_chance = erase_chance
            # CHECK IF BUILD CONDITIONS are favorable
            build_condition = agent.check_build_conditions(ground)
            if agent.build_chance >= reach_to_build and build_condition == True:
                done = agent.build(ground)
                done2 = agent.build(clay_moisture_layer)
                if done:
                    reset_agent = True
            elif agent.erase_chance >= reach_to_erase and build_condition == True:
                done = agent.erase(ground)
                done2 = agent.erase(clay_moisture_layer)
                pass
        
        elif not moved:
            # stuck in position: reset
            reset_agent = True
        
        if reset_agent:
            x = np.random.randint(0, voxel_size)
            y = np.random.randint(0, voxel_size)
            agent.pose = [x,y,1]
            agent.build_probability = 0
            agent.move_history = []

    print('done')

    # 3. SHOW (without ground layer)
    a1 = ground.array.copy()
    a1[:,:,0] = 0

    # scatter plot
    pts_built = convert_array_to_points(a1, False)
    arrays_to_show = [pts_built]
    colors = [ground.rgb]
    for array, color in zip(arrays_to_show, colors):
        p = array.transpose()
        axes.scatter(p[0, :], p[1, :], p[2, :], marker = 's', s = 1, facecolor = color)
    iterate.counter += 1

scale = voxel_size
fig = plt.figure(figsize = [4, 4], dpi = 200)
axes = plt.axes(xlim=(0, scale), ylim =  (0, scale), zlim = (0, scale), projection = '3d')
axes.set_xticks([])
axes.set_yticks([])
axes.set_zticks([])
# a1 = ground.array
# a1[:,:,0] = 0
# ground.array = a1
p = ground.array.transpose()
axes.scatter(p[0, :], p[1, :], p[2, :], marker = 's', s = 1, facecolor = ground.rgb)

iterate.counter = 0
anim = animation.FuncAnimation(fig, iterate, frames=iterations, interval = 1)
if save_animation:
    anim.save('img/gif/%s_%s_%s.gif' %(title_, timestamp_now, note))
    print('animation saved')
if save_:
    plt.savefig('img/%s_%s_%s.png' %(title_, timestamp_now, note), bbox_inches='tight', dpi = 200)
    print('image saved')

# # save as point_list
if save_json:
    filename = 'scr/data/point_lists/pts_%s_%s.json' %(time__, note)
    with open(filename, 'w') as file:
        # list_to_dump = convert_array_to_points(ground.array, True)
        list_to_dump = convert_array_to_compas_pointcloud_sorted(clay_moisture_layer.array, clay_moisture_layer.array)
        json.dump(list_to_dump, file)
    print('\npt_list saved as %s:\n' %filename)

plt.show()