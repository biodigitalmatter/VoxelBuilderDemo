from voxel_builder_library import *
from show_voxel_plt import *


voxel_size = 40
agent_count = 4
iterations = 40
save_ = True
title_ = 'img'
note = 'queen_ph'

agent_space = Layer(voxel_size=voxel_size, rgb=[0.5,0.5,0.5])
queen_space = Layer(voxel_size=voxel_size, rgb=[0.5,0.5,0.5])
track_layer = Layer(voxel_size=voxel_size, rgb=[.09,.08,0])
smell_layer = Layer(voxel_size=voxel_size, rgb=[0.1,0.1,0.1], diffusion_ratio=1/7, decay_ratio=0.2)
offset_ph = Layer(name = 'offset_ph', voxel_size=voxel_size, rgb = [0.25, 0.25, 0.25])

# create ground:
ground_level_Z = 0
ground = Layer(voxel_size=voxel_size, name='Ground')
ground.array = make_solid_box_z(voxel_size, ground_level_Z)
wall = make_solid_box_xxyyzz(voxel_size, 12,12,0,20,0,6)
ground.array += wall
ground.rgb = [0.025,0.025,0.025]

# grounds_offset
offset_ph.decay_linear_value = 1/6
offset_ph.decay_ratio = 0
offset_ph.diffusion_ratio = 1/3
grounds_emission_value = 2

# make agents
agents = []
for i in range(agent_count):
    agent = Agent(
        space_layer = agent_space, ground_layer = ground, limited_to_ground = 'offset', track_layer = track_layer, leave_trace=True)
    x = np.random.randint(0, voxel_size)
    y = np.random.randint(0, voxel_size)
    agent.pose = [x,y,1]
    agent.leave_trace = True
    agents.append(agent)
queen = Agent(
    space_layer = queen_space, ground_layer = ground)
queen.pose = [20,20,1]
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
    offset_ph.emission_intake(ground.array, grounds_emission_value, False)
    offset_ph.diffuse(False)
    offset_ph.decay_linear()
    smell_layer.emission_intake(queen_space.array, 1, False)
    smell_layer.diffuse()
    smell_layer.decay()
    ground.block_layers([smell_layer])
    #follow pheromones
    for agent in agents:
        pheromones = agent.get_nb_cell_values(smell_layer, agent.pose)
        # print(pheromones)
        agent.follow_pheromones(pheromones, offset_ph)
    # path_pheromone
    # smell_layer.emission_intake(agent_space.array, 1, False)
    


# add layers and layer_colors
c1 = ground.color_array
c2 = agent_space.color_array
c3 = queen_space.color_array
c4 = track_layer.color_array
colors = (c1 + c2 + c3 + c4) /4

# show image
f,a = init_fig(suffix=note)  #bottom_line=Layer.__str__())
show_voxel(f,a, queen_space.array + ground.array + agent_space.array + track_layer.array , save=True, suffix=note)
# show_voxel(f,a, smell_layer.array, c4, save=True, suffix=note)