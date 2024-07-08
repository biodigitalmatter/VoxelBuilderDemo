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
save_json_in_steps = False
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
sky_ph_layer.gradient_resolution = 0.001

clay_moisture_layer.diffusion_ratio = 0
air_moisture_layer.decay_ratio = 1/12
air_moisture_layer.gradient_resolution = 0.001

air_moisture_layer.diffusion_ratio = 1/12
air_moisture_layer.decay_ratio = 1/4
air_moisture_layer.gradient_resolution = 0.001

# MOVE SETTINGS
# move_preference settings w pheromon weights
ground_smell_ph_w = 0
random_ph_w = 0.2
move_ph_sky = 1
move_ph_moisture = 0.2
move_prefer_to_side = 0.5
move_prefer_to_up = 1
move_prefer_to_down = -0.2

# BUILD SETTINGS
construction_on = True
reach_to_build = 2

# build by last move settings
climb = 0.5
top = 2
walk = 0.1
descend = -0.05
build_strength__last_move = 0
def build_by_last_move(
        agent, 
        build_strength__last_move = 0, 
        climb = 0.5,
        top = 2,
        walk = 0.1,
        descend = -0.05,):
    pass

# build by relative position
build_below = -1
build_aside = -1
build_above = 1
build_strength__relative_position = 0
def build_by_relative_position(
        agent,
        build_strength = 1,
        build_below = -1,
        build_aside = -1,
        build_above = 1,):
    pass

# build by density : ground
# NOTE this could be directional scanning
erase_if_over__ground = 20
build_if_below__ground = 5
build_strength__ground = 0
def build_or_erase_by_density(
        agent, 
        layer,
        radius,
        erase_if_over = 20,
        build_if_below = 5,
        build_strength = 1):
    pass

# build by pheromone density
build_if_over__queen_bee = 0.005
build_if_below__queen_bee = 0.05
build_strength__queen_bee_ph = 0
def build_by_density(
        agent, 
        layer,
        radius,
        build_if_over = 20,
        build_if_below = 5,
        build_strength = 1):
    pass

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


def pheromon_loop(pheromon_layer, emmission_array = None, i = 1, blocking_layer = None, gravity_direction = None, gravity_ratio = None, grade_bool = False):
    """gravity direction: 0:left, 1:right, 2:front, 3:back, 4:down, 5:up"""
    for i in range(i):
        if emmission_array != None:
            pheromon_layer.emission_intake(emmission_array, 2, False)
        pheromon_layer.diffuse()
        if gravity_direction != None and gravity_ratio != None:
            pheromon_layer.gravity_shift(gravity_direction, gravity_ratio)
        pheromon_layer.decay()
        if blocking_layer != None:
            blocking_layer.block_layers([pheromon_layer])
        if grade_bool:
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
pheromon_loop(clay_moisture_layer, None, 3)
pheromon_loop(air_moisture_layer, )

# make sky
# sky_ph_layer
sky_emission = np.zeros(voxel_size, voxel_size, voxel_size)
sky_emission[:][:][voxel_size - 1] = 1
pheromon_loop(sky_ph_layer, sky_emission, wait_to_diffuse, blocking_layer=ground, gravity_shift_p = [5, 0.8])



# run as simulation
def animate(frame):
# for i in range(iterations):
    print(animate.counter)

    # diffuse layers
    pheromon_loop(sky_ph_layer, blocking_layer=ground)


    # move and build
    for agent in agents:
        reset_agent = False
        queen_smell_ph = agent.get_nb_26_cell_values(sky_ph_layer, agent.pose) * ground_smell_ph_w
        random_ph = agent.random_pheromones(26) * random_ph_w
        up_pref_ph = agent.direction_preference_26_pheromones(move_prefer_to_side) * move_prefer_to_up
        pheromone_cube = random_ph * 2 + queen_smell_ph + up_pref_ph * 0.5
        moved = agent.follow_pheromones(pheromone_cube)

        # move based on climb style
        if moved:
            # check move style
            # agent.analyze_move_history()
            # add probability per style
            agent.add_build_propability_by_pheromone_density(
                queen_smell_ph, 
                build_strength__queen_bee_ph, 
                build_min_ph_density__queen_bee, 
                build_max_ph_density__queen_bee)
            agent.add_build_probability_by_move_history(add_prob, climb, top, walk, descend)
            below, aside, above = agent.analyze_position(ground)
            if below: agent.build_probability += build_below
            if aside: agent.build_probability += build_aside
            if above: agent.build_probability += build_above
            # build
            if construction_on:
                # CHECK IF BUILD CONDITIONS are favorable
                build_condition = agent.check_build_conditions(ground)
                if agent.build_probability >= build_probability_limit and build_condition == True:
                    built = agent.build()
                    if built:
                        reset_agent = True
        
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

    # SHOW (without ground layer)
    a1 = ground.array.copy()
    a1[:,:,0] = 0

    # show SCATTER PLOT
    pts_built = convert_array_to_points(a1, False)
    # pts_agent_space = convert_array_to_points(agent_space.array, False)
    arrays_to_show = [pts_built]
    colors = [ground.rgb]
    # arrays_to_show = [pts_built, pts_agent_space]
    # colors = [ground.rgb, agent_space.rgb]
    for array, color in zip(arrays_to_show, colors):
        p = array.transpose()
        axes.scatter(p[0, :], p[1, :], p[2, :], marker = 's', s = 1, facecolor = color)
    c = animate.counter
    # # save as point_list
    if save_json_in_steps:
        if c % 5 == 0:
            filename = 'scr/data/point_lists/pts_built_%s_%s_i-%s.json' %(time__, note, c)
            with open(filename, 'w') as file:
                list_to_dump = convert_array_to_points(ground.array, True)
                json.dump(list_to_dump, file)
            print('\nptlist saved as %s:\n' %filename)
    
    animate.counter += 1

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

animate.counter = 0
anim = animation.FuncAnimation(fig, animate, frames=iterations, interval = 1)
# if save_animation:
#     anim.save('img/gif/%s_%s_%s.gif' %(title_, timestamp_now, note))
#     print('saved_anim')
if save_:
    plt.savefig('img/%s_%s_%s.png' %(title_, timestamp_now, note), bbox_inches='tight', dpi = 200)
    print('saved img')

# # save as point_list
if save_:
    filename = 'scr/data/point_lists/pts_%s_%s.json' %(time__, note)
    with open(filename, 'w') as file:
        list_to_dump = convert_array_to_points(ground.array, True)
        json.dump(list_to_dump, file)
    print('\nptlist saved as %s:\n' %filename)

plt.show()