from voxel_builder_library import *
from show_voxel_plt import *


voxel_size = 20
agent_count = 10
iterations = 40
save_ = False
title_ = 'img'
note = 'queen_ph'

agent_space = Layer(voxel_size=voxel_size, rgb=[0.1,0.02,0.02])
queen_space = Layer(voxel_size=voxel_size, rgb=[0.2,0,0.04])
track_layer = Layer(voxel_size=voxel_size, rgb=[.09,.08,0])
smell_layer = Layer(voxel_size=voxel_size, rgb=[0.001,0.001,0.001], diffusion_ratio=1/7, decay_ratio=0.2)
# offset_pheromone = Layer(name = 'offset_pheromone', voxel_size=voxel_size, rgb = [0.25, 0.25, 0.25])

# create ground:
ground_level_Z = 0
ground = Layer(voxel_size=voxel_size, name='Ground')
ground.array = make_solid_box_z(voxel_size, ground_level_Z)
# wall = make_solid_box_xxyyzz(voxel_size, 18,18,0,20,0,12)
ground.rgb = [0.25,0.25,0.2]

# # grounds_offset
# offset_pheromone.decay_linear_value = 1/6
# offset_pheromone.decay_ratio = 0
# offset_pheromone.diffusion_ratio = 1/3
# grounds_emission_value = 2

# make agents
agents = []
for i in range(agent_count):
    agent = Agent(
        space_layer = agent_space, ground_layer = ground, walk_on_ground = True, track_layer = track_layer)
    x = np.random.randint(0, voxel_size)
    y = np.random.randint(0, voxel_size)
    agent.pose = [x,y,1]
    agent.leave_trace = True
    agents.append(agent)
queen = Agent(
    space_layer = queen_space, ground_layer = ground, walk_on_ground = True)
queen.pose = [10,10,1]
# queen.move_key('left')
queen.update_space()
# queen_space.array[10,10,1] = 1

# prep smells
for i in range(15):
    smell_layer.emission_intake(queen_space.array, 1, False)
    smell_layer.diffuse()
    smell_layer.decay()
    ground.block_layers([smell_layer])

# run simulation
for i in range(iterations):
    # offset_pheromone.emissision_intake(ground.array, grounds_emission_value, False)
    # offset_pheromone.diffuse(False)
    # offset_pheromone.decay_linear()
    smell_layer.emission_intake(queen_space.array, 1, False)
    smell_layer.diffuse()
    smell_layer.decay()
    ground.block_layers([smell_layer])
    #follow pheromones
    for agent in agents:
        pheromones = agent.get_nb_cell_values(smell_layer, agent.pose)
        # print(pheromones)
        agent.follow_pheromones(pheromones)
    # path_pheromone
    # smell_layer.emission_intake(agent_space.array, 1, False)
    


# add layers and layer_colors
c1 = ground.color_array
c2 = agent_space.color_array
c3 = queen_space.color_array
c4 = track_layer.color_array
# c4 = smell_layer.color_array
# c4 = offset_pheromone.color_array
colors = (c2 + c3 + c4) / 3
colors = agent_space.color_array
show_layer = agent_space.array # + queen_space.array #+ track_layer.array

# show image
f,a = init_fig(suffix=note)  #bottom_line=Layer.__str__())
show_voxel(f,a, show_layer, colors, save=True, suffix=note)
# show_voxel(f,a, smell_layer.array, c4, save=True, suffix=note)