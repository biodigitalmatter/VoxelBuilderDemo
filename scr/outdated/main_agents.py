from voxel_builder_library import *
from show_voxel_plt import *
from class_agent import Agent
from class_layer import Layer


voxel_size = 10
agent_count = 1
iterations = 2
save_ = True
title_ = 'img'
note = 'fixed_colors_inverted_pheromon_inversecolors'

gravity_option = ['nb_check', 'offset_ph', 'cube_corner_nb_check', 'cube_edge_nb_check'][2]

construction_on = False
construct_limit_1 = 0.001
construct_limit_2 = 0.01
wait = 1

agent_space = Layer(voxel_size=voxel_size, rgb=[34/255, 116/255, 240/255])
queen_space = Layer(voxel_size=voxel_size, rgb=[203/255, 21/255, 207/255])
track_layer = Layer(voxel_size=voxel_size, rgb=[147/255, 209/255, 237/255])
smell_layer = Layer(voxel_size=voxel_size, rgb=[240/255, 220/255, 150/255], diffusion_ratio=1/6, decay_ratio=0.01)
ground = Layer(voxel_size=voxel_size)
# create ground:
ground_level_Z = 0
ground.array = make_solid_box_z(voxel_size, ground_level_Z)
wall = make_solid_box_xxyyzz(voxel_size, 12,16,10,40,0,4)
ground.array += wall
ground.rgb = [135/255, 126/255, 119/255]

# # grounds_offset
# offset_ph = Layer(name = 'offset_ph', voxel_size=voxel_size, rgb = [0.25, 0.25, 0.25])
# offset_ph.decay_linear_value = 1/6
# offset_ph.decay_ratio = 0
# offset_ph.diffusion_ratio = 1/3
# grounds_emission_value = 2

# make agents
agents = []
for i in range(agent_count):
    agent = Agent(
        space_layer = agent_space, ground_layer = ground, construction_layer = ground,
        limited_to_ground = gravity_option, track_layer = track_layer, leave_trace=False, save_move_history=True)
    x = np.random.randint(0, voxel_size)
    y = np.random.randint(0, voxel_size)
    agent.pose = [x,y,1]
    agent.rgb = [1,0,0]
    agent.leave_trace = True
    agents.append(agent)

# make queen
queen = Agent(space_layer = queen_space, ground_layer = ground)
queen.pose = [1,1,1]
queen.update_space()
queen.rgb = [0.25,0.25,0]

# pre_smells
# for i in range(wait):
#     smell_layer.emission_intake(queen_space.array, 2, False)
#     smell_layer.diffuse()
#     smell_layer.decay()
#     ground.block_layers([smell_layer])

# run simulation
for i in range(iterations):
    # # offset layer
    # offset_ph.emission_intake(ground.array, grounds_emission_value, False)
    # offset_ph.diffuse(False)
    # offset_ph.decay_linear()

    # queen odor
    smell_layer.emission_intake(queen_space.array, 2, False)
    smell_layer.diffuse()
    smell_layer.decay()
    ground.block_layers([smell_layer])

    #follow pheromones
    # print(i)
    for agent in agents:
        pheromones = agent.get_nb_cell_values(smell_layer, agent.pose)
        random_ph = agent.random_pheromones() * 0.1
        up_pref = agent.direction_preference_pheromones(0.9) * 0.15
        # agent.follow_pheromones(pheromones + random_ph + up_pref, offset_limit = offset_ph)
        # agent.follow_pheromones(random_ph + up_pref)
        agent.follow_pheromones(random_ph + up_pref)
        if construction_on:
            # build after history
            flag = agent.get_build_flag_after_history(
                last_step_NOR = ['up', 'down'], last_step_len = 3,
                previous_steps_AND = ['up', 'up', 'up'])
            # build after pheromones
            # flag = agent.get_build_flag_after_pheromones(smell_layer, construct_limit_1, construct_limit_2)
            if flag:
                built = agent.build()
                #reset_position
                if built:
                    x = np.random.randint(0, voxel_size)
                    y = np.random.randint(0, voxel_size)
                    agent.pose = [x,y,1]
        
    
    # print(len(agents))
    # make path_pheromone
    # smell_layer.emission_intake(agent_space.array, 1, False)
    
# print(agents[0].move_history)

# add layers and layer_colors
c1 = ground.color_array
c2 = agent_space.color_array
c3 = queen_space.color_array
c4 = track_layer.color_array
# c5 = smell_layer.color_array_inverse

a1 = ground.array
a2 = agent_space.array
a3 = queen_space.array
a4 = track_layer.array
# a5 = smell_layer.array

# show image
f,a = init_fig(suffix=note)  #bottom_line=Layer.__str__())
show_voxel(f,a, a1 + a2 + a3 + a4, c1 + c2 + c3 + c4, save=True, suffix=note)
# show_voxel(f,a, smell_layer.array, c4, save=True, suffix=note)