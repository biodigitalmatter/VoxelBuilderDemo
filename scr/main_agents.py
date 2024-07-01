from voxel_builder_library import *
from show_voxel_plt import *


voxel_size = 20
agent_count = 2
iterations = 2
save_ = False
title_ = 'img'
note = 'wall_1'

agent_space = Layer(voxel_size=voxel_size, rgb=[0.2,0,0.2])
track_layer = Layer(voxel_size=voxel_size, rgb=[.5,0,0])
smell_layer = Layer(voxel_size=voxel_size, rgb=[0.001,0.001,0.001], decay_linear_value=0.01, diffusion_ratio=0.5)

# create ground:
ground_level_Z = 1
ground = Layer(voxel_size=voxel_size, name='Ground')
a = make_solid_box_z(voxel_size, 2)
b = make_solid_box_xxyyzz(voxel_size, 2,2,0,20,0,12)
ground.array += a + b
ground.rgb = [0.5,0.5,0.5]

# make agents
agents = []
for i in range(agent_count):
    agent = Agent(
        space_layer = agent_space,
        track_layer=None,
        leave_trace=False,
        ground_layer=ground, 
        walk_on_ground=True)
    # agent.pose = [np.random.randint(0, voxel_size,[3])]
    x = np.random.randint(0, voxel_size)
    y = np.random.randint(0, voxel_size)
    agent.pose = [x, y, ground_level_Z]
    agents.append(agent)

# run simulation
for i in range(iterations):
    for agent in agents:
        #follow random pheromones
        random_pheromones = agent.random_pheromones()
        choice = random_pheromones
        agent.follow_pheromones(choice)
    # smell_layer.emissision_intake(agent_space.array, 1, False)
    # smell_layer.diffuse()
    # smell_layer.decay_linear()
        

# add layers and layer_colors
c1 = ground.color_array
c2 = agent_space.color_array
# c3 = track_layer.color_array
c4 = smell_layer.color_array

show_layer = ground.array + agent_space.array + smell_layer.array
show_layer_colors = np.minimum(c1 + c2 + c4, 1)
# show_layer_colors = c1 + c2 + c3
# show image
f,a = init_fig(suffix=note)
show_voxel(f,a, show_layer, show_layer_colors, save=True, suffix=note)
# show_voxel(f,a, smell_layer.array, c4, save=True, suffix=note)