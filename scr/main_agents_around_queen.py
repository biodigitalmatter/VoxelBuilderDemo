from voxel_builder_library import *
from show_voxel_plt import *
from helpers import *
from show_voxel_plt import timestamp_now


voxel_size = 30
agent_count = 20
iterations = 800
save_ = True
title_ = 'img'
note = 'test_26_nbs'

walk_method_option = ['nb_check', 'offset_ph', 'cube_corner_nb_check', 'cube_edge_nb_check'][2]

construction_on = True
# construct_limit_1 = 0.01
# construct_limit_2 = 0.09
construct_limit_1 = 0.005
construct_limit_2 = 0.05
wait = 50
check_collision = False

agent_space = Layer(voxel_size=voxel_size, rgb=[34/255, 116/255, 240/255])
queen_space = Layer(voxel_size=voxel_size, rgb=[203/255, 21/255, 207/255])
# track_layer = Layer(voxel_size=voxel_size, rgb=[147/255, 209/255, 237/255])
smell_layer = Layer(voxel_size=voxel_size, rgb=[240/255, 220/255, 150/255], diffusion_ratio=1/6, decay_ratio=0.01)

# create ground:
ground_level_Z = 0
ground = Layer(voxel_size=voxel_size, name='Ground')
ground.array = make_solid_box_z(voxel_size, ground_level_Z)
# wall = make_solid_box_xxyyzz(voxel_size, 3,5,2,8,0,12)
# ground.array += wall
ground.rgb = [207/255, 179/255, 171/255]

# grounds_offset
offset_ph = Layer(name = 'offset_ph', voxel_size=voxel_size)
offset_ph.decay_linear_value = 1/6
offset_ph.decay_ratio = 0
offset_ph.diffusion_ratio = 1/3
grounds_emission_value = 2

# make agents
agents = []
for i in range(agent_count):
    agent = Agent(
        space_layer = agent_space, ground_layer = ground, construction_layer = ground,
        track_layer = None, leave_trace=False, save_move_history=False)
    x = np.random.randint(0, voxel_size)
    y = np.random.randint(0, voxel_size)
    agent.pose = [x,y,1]
    agents.append(agent)

# make queen
queens = []
poses = [[20,20], [12,9]]
for i in range(2):
    queen = Agent(space_layer = queen_space, ground_layer = ground)
    x,y = poses[i]
    queen.pose = [x,y,1]
    queen.update_space()

# pre_smells
for i in range(wait):
    smell_layer.emission_intake(queen_space.array, 2, False)
    smell_layer.diffuse()
    smell_layer.gravity_shift(5, 1)
    smell_layer.decay()
    ground.block_layers([smell_layer])

# run simulation
for i in range(iterations):
    # queen odor
    smell_layer.emission_intake(queen_space.array, 2, False)
    smell_layer.diffuse()
    smell_layer.gravity_shift(5, 1)
    smell_layer.decay()
    ground.block_layers([smell_layer])

    #follow pheromones
    for agent in agents:
        # Agent.get_nb_26_cell_values
        queen_ph = agent.get_nb_26_cell_values(smell_layer, agent.pose)
        random_ph = agent.random_pheromones(26)
        up_pref_ph = agent.direction_preference_26_pheromones(0.8)
        pheromone_cube = random_ph * 2 + queen_ph * 0.1 + up_pref_ph * 0.5
        moved = agent.follow_pheromones(pheromone_cube)
        if moved:
            # build
            if construction_on:
                flag = agent.get_build_flag_by_pheromones(smell_layer, construct_limit_1, construct_limit_2 )
                if flag:
                    built = agent.build()
                else: built = False
                if built: # reset position
                    x = np.random.randint(0, voxel_size)
                    y = np.random.randint(0, voxel_size)
                    # print(x,y)
                    agent.pose = [x,y,1]
        else:
            # couldnt move (stuck) position reset
            agent.pose = [x,y,1]

print('done')
# show smell layer in limits
# a5 = smell_layer.array
# smell_layer.array = np.where(construct_limit_1 <= a5, a5, 0)
# smell_layer.array = np.where(construct_limit_2 >= smell_layer.array, smell_layer.array, 0)


# add layers and layer_colors
c1 = ground.color_array
c2 = agent_space.color_array
c3 = queen_space.color_array
c5 = smell_layer.color_array_inverse

a1 = ground.array
a2 = agent_space.array
a3 = queen_space.array
# a4 = track_layer.array
a5 = smell_layer.array
# a1[:,:,0] = 0
ground.array = a1

time__ = timestamp_now
# # save as pointcloud
# filename = 'scr/data/compas_pointclouds/ptcloud_%s_%s.json' %(time__, note)
# ptcloud = convert_array_to_compas_pointcloud(a1)
# save_ptcloud(ptcloud, filename)
# print('ptcloud saved as %s:' %filename)

# # save as point_list
if save_:
    filename = 'scr/data/point_lists/pts_%s_%s.json' %(time__, note)
    with open(filename, 'w') as file:
        list_to_dump = convert_array_to_points(ground.array, True)
        json.dump(list_to_dump, file)
    print('\nptlist saved as %s:\n' %filename)


# show VOXEL image
# f,a = init_fig(suffix=note)  #bottom_line=Layer.__str__())
# show_voxel(f,a, a1 + a2 + a3, c1 + c2 + c3, save=save_, suffix=note)
# show_voxel(f,a, a1 + a2 + a3 + a5, c1 + c2 + c3 + c5, save=True, suffix=note)
# show_voxel(f,a, a1 + a5, c1 + c5, save=save_, suffix=note + '_smells')
# show_voxel(f,a, a1 + a3, c1 + c3, save=save_, suffix=note)

# show SCATTER PLOT
pts_ground = convert_array_to_points(ground.array, False)
pts_agent_space = convert_array_to_points(agent_space.array, False)

arrays_to_show = [pts_ground, pts_agent_space]
colors = [ground.rgb, agent_space.rgb]

scale = voxel_size
axes = plt.axes(xlim=(0, scale), ylim =  (0, scale), zlim = (0, scale), projection = '3d')
axes.set_xticks([])
axes.set_yticks([])
axes.set_zticks([])
for array, color in zip(arrays_to_show, colors):
    p = array.transpose()
    axes.scatter(p[0, :], p[1, :], p[2, :], marker = 's', s = 10, facecolor = color)
plt.savefig('img/%s_%s_%s.png' %(title_, timestamp_now, note), bbox_inches='tight', dpi = 200)
print('saved')
plt.show()