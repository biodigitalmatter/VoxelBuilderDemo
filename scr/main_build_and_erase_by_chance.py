from voxel_builder_library import *
from show_voxel_plt import *
from helpers import *
from show_voxel_plt import timestamp_now
from matplotlib import animation

# import presets from here
from agent_algorithms import *


iterations = 200

note = 'test_work_w_agent_algorithms'
time__ = timestamp_now
_save = True

# SETUP ENVIRONMENT
voxel_size, agent_count, ground, queen_bee_pheromon, sky_ph_layer, sky_emission_layer, clay_moisture_layer, air_moisture_layer, agent_space = layer_env_setup(iterations)

# make agents
agents = []
for i in range(agent_count):
    agent = Agent(
        space_layer = agent_space, ground_layer = ground,
        track_layer = None, leave_trace=False, save_move_history=True)
    x = np.random.randint(0, voxel_size)
    y = np.random.randint(0, voxel_size)
    agent.pose = [x,y,1]
    agents.append(agent)

# SIMULATION FUNCTION
def simulate(frame):
# for i in range(iterations):
    print('simulate.counter', simulate.counter)

    # 1. diffuse environment's layers
    pheromon_loop(sky_ph_layer, emmission_array = sky_emission_layer, blocking_layer=ground, gravity_shift_bool = True)
    pheromon_loop(air_moisture_layer, emmission_array = clay_moisture_layer.array, blocking_layer = ground)

    # 2. MOVE and BUILD
    for agent in agents:
        print('agent chances: ', agent.build_chance, agent.erase_chance)
        print('pose:', agent.pose)
        # MOVE
        moved = move_agent(agent, queen_bee_pheromon, sky_ph_layer, air_moisture_layer)
        # BUILD
        if moved:
            build_chance, erase_chance = calculate_build_chances(agent, ground, queen_bee_pheromon, air_moisture_layer, sky_ph_layer)
            
            built, erased = build(agent, build_chance, erase_chance, ground, clay_moisture_layer)
            if erased:
                print('erase here:', agent.pose)

            if built and go_home_after_build:
                print('built here:', agent.pose)
                reset_agent(agent, voxel_size)
        else:
            if go_home_after_build:
                reset_agent(agent, voxel_size)

    print('agents_done')
    ground.decay_linear()

    # 3. SHOW without ground layer
    a1 = ground.array.copy()
    a1[:,:,0] = 0

    # scatter plot
    pts_built = convert_array_to_points(a1, False)
    # pts_built_2 = convert_array_to_points(agent_space.array, False)

    arrays_to_show = [pts_built]
    colors = [ground.rgb]
    for array, color in zip(arrays_to_show, colors):
        p = array.transpose()
        axes.scatter(p[0, :], p[1, :], p[2, :], marker = 's', s = 1, facecolor = color)
    simulate.counter += 1

### PLOTTING
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

simulate.counter = 0
anim = animation.FuncAnimation(fig, simulate, frames=iterations, interval = 1)
suffix = '%s_a%s_i%s' %(note, agent_count, iterations)

### SAVE
save_img = _save
save_animation = _save
save_json = _save

if save_animation:
    anim.save('img/gif/gif_%s_%s.gif' %(timestamp_now, suffix))
    print('animation saved')
if save_img:
    plt.savefig('img/img_%s_%s.png' %(timestamp_now, suffix), bbox_inches='tight', dpi = 200)
    print('image saved')

if save_json:
    # filename = 'scr/data/point_lists/pts_%s_%s.json' %(time__, note)
    filename = 'scr/data/point_lists_sorted/pts_%s_%s_CLAY_w_decay.json' %(time__, note)
    with open(filename, 'w') as file:
        # list_to_dump = convert_array_to_points(ground.array, True)
        # list_to_dump = convert_array_to_pts_sorted(ground.array)
        list_to_dump = convert_array_to_pts_sorted(clay_moisture_layer.array, multiply=1000)

        # list_to_dump = convert_array_to_pts_sorted(ground.array)
        json.dump(list_to_dump, file)
    print('\npt_list saved as %s:\n' %filename)

plt.show()