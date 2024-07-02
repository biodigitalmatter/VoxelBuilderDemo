from voxel_builder_library import *
from show_voxel_plt import *


voxel_size = 40
agent_count = 2
iterations = 50
save_ = False
title_ = 'img'
note = 'queen_ph_after_50'

gravity_option = ['nb_check', 'offset_ph', 'cube_corner_nb_check', 'cube_edge_nb_check'][3]

construction_on = True
construct_limit_1 = 0.001
construct_limit_2 = 0.002
wait = 50

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
ground.rgb = [135/255, 126/255, 119/255]

# make agents
agents = []
for i in range(agent_count):
    agent = Agent(
        space_layer = agent_space, ground_layer = ground, construction_layer = ground,
        limited_to_ground = gravity_option, track_layer = None, leave_trace=False, save_move_history=False)
    x = np.random.randint(0, voxel_size)
    y = np.random.randint(0, voxel_size)
    agent.pose = [x,y,1]
    agents.append(agent)

# make queen
queen = Agent(space_layer = queen_space, ground_layer = ground)
queen.pose = [20,20,2]
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
    smell_layer.decay()
    ground.block_layers([smell_layer])

    #follow pheromones
    for agent in agents:
        queen_pheromones = agent.get_nb_cell_values(smell_layer, agent.pose) * 0.6
        random_ph = agent.random_pheromones() * 0.1
        # up_pref = agent.direction_preference_pheromones(0.7) * 0.005
        agent.follow_pheromones(random_ph + queen_pheromones)
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

# show smell layer in limits
a5 = smell_layer.array
smell_layer.array = np.where(construct_limit_1 <= a5, a5, 0)
# smell_layer.array = np.where(construct_limit_2 <= smell_layer.array, a5, 0)


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

# show image
f,a = init_fig(suffix=note)  #bottom_line=Layer.__str__())
# show_voxel(f,a, a1 + a2 + a3, c1 + c2 + c3, save=True, suffix=note)
show_voxel(f,a, a1 + a2 + a3 + a5, c1 + c2 + c3 + c5, save=True, suffix=note)
# show_voxel(f,a, a5, c5, save=True, suffix=note + '_smells')
# show_voxel(f,a, a1 + a3, c1 + c3, save=True, suffix=note)