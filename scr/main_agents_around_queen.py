from voxel_builder_library import *
from show_voxel_plt import *


voxel_size = 30
agent_count = 10
iterations = 5000
save_ = True
title_ = 'img'
note = 'build_after_queen_ph-tests_from_corner'

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
# wall = make_solid_box_xxyyzz(voxel_size, 12,12,0,40,0,25)
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
        limited_to_ground = walk_method_option, track_layer = None, leave_trace=False, save_move_history=False)
    x = np.random.randint(0, voxel_size/10)
    y = np.random.randint(0, voxel_size/10)
    agent.pose = [x,y,1]
    agents.append(agent)

# make queen
queens = []
for i in range(1):
    queen = Agent(space_layer = queen_space, ground_layer = ground)
    # x = np.random.randint(5, voxel_size - 5)
    # y = np.random.randint(5, voxel_size - 5)
    x,y = [22,22]
    agent.pose = [x,y,1]
    queen.pose = [x,y,1]
    queen.update_space()

# pre_smells
for i in range(wait):
    smell_layer.emission_intake(queen_space.array, 2, False)
    smell_layer.diffuse()
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
        queen_pheromones = agent.get_nb_cell_values(smell_layer, agent.pose) * 2
        random_ph = agent.random_pheromones() * 0.1
        up_pref = agent.direction_preference_pheromones(0.9) * 0.5
        agent.follow_pheromones(random_ph + queen_pheromones + up_pref, offset_ph, check_collision)
        # build
        if construction_on:
            flag = agent.get_build_flag_after_pheromones(smell_layer, construct_limit_1, construct_limit_2 )
            if flag:
                built = agent.build()
            else: built = False
            if built: # reset position
                x = np.random.randint(0, voxel_size)
                y = np.random.randint(0, voxel_size)
                # print(x,y)
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
a1[:,:,0] = 0
# show image
f,a = init_fig(suffix=note)  #bottom_line=Layer.__str__())
# show_voxel(f,a, a1 + a2 + a3, c1 + c2 + c3, save=save_, suffix=note)
# show_voxel(f,a, a1 + a2 + a3 + a5, c1 + c2 + c3 + c5, save=True, suffix=note)
# show_voxel(f,a, a5, c5, save=save_, suffix=note + '_smells')
show_voxel(f,a, a1 + a3, c1 + c3, save=save_, suffix=note)