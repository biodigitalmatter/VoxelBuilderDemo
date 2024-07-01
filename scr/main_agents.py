from voxel_builder_library import *
from show_voxel_plt import *


voxel_size = 20
agent_count = 1
iterations = 200
save_ = False
title_ = 'img'
note = 'ground_distance_ph-i200-decay1to6-diffusion1to3-groundE2'

agent_space = Layer(voxel_size=voxel_size, rgb=[0.2,0,0.2])
track_layer = Layer(voxel_size=voxel_size, rgb=[.5,0,0])
smell_layer = Layer(voxel_size=voxel_size, rgb=[0.001,0.001,0.001], decay_linear_value=0.0001, diffusion_ratio=1, decay_ratio=0)
offset_pheromone = Layer(name = 'offset_pheromone', voxel_size=voxel_size, rgb = [0.25, 0.25, 0.25])
# create ground:
ground_level_Z = 1
ground = Layer(voxel_size=voxel_size, name='Ground')
a = make_solid_box_z(voxel_size, 0)
b = make_solid_box_xxyyzz(voxel_size, 18,18,0,20,0,12)
ground.array += a + b
ground.rgb = [0.5, 0.5, 0.5]

offset_pheromone.decay_linear_value = 1/6
offset_pheromone.decay_ratio = 0
offset_pheromone.diffusion_ratio = 1/3
grounds_emission_value = 2

# make agents
agents = []
for i in range(agent_count):
    agent = Agent(
        space_layer = agent_space,
        track_layer=None,
        leave_trace=False,
        ground_layer=ground, 
        walk_on_ground=True)
    x = np.random.randint(0, voxel_size)
    y = np.random.randint(0, voxel_size)
    # agent.pose = [x, y, ground_level_Z]
    agent.pose = [15,3,2]
    agents.append(agent)

# run simulation
for i in range(iterations):
    offset_pheromone.emissision_intake(ground.array, grounds_emission_value, False)
    offset_pheromone.diffuse(False)
    offset_pheromone.decay_linear()
    for agent in agents:
        #follow random pheromones
        random_pheromones = agent.random_pheromones()
        choice = random_pheromones
        agent.follow_pheromones(choice)
    smell_layer.emissision_intake(agent_space.array, 1, False)
    smell_layer.diffuse()
    # ground.block_layers([smell_layer, offset_pheromone])

    smell_layer.decay_linear()

# add layers and layer_colors
c1 = ground.color_array
c2 = agent_space.color_array
# c3 = track_layer.color_array
# c4 = smell_layer.color_array
c4 = offset_pheromone.color_array
colors = c1 + c4 / 2

show_layer = ground.array + offset_pheromone.array
# show image
f,a = init_fig(suffix=note, bottom_line=offset_pheromone.__str__())
show_voxel(f,a, show_layer, colors, save=True, suffix=note)
# show_voxel(f,a, smell_layer.array, c4, save=True, suffix=note)