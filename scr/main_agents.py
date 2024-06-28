from voxel_builder_library import *
from show_voxel_plt import *


voxel_size = 6
agent_count = 15
iterations = 15

agent_space = Layer(voxel_size=voxel_size, rgb=[0.2,0,0.2])
track_layer = Layer(voxel_size=voxel_size, rgb=[.5,0,0])

# create ground:
ground_level_Z = 1
ground = Layer(voxel_size=voxel_size)
i = np.arange(voxel_size)
underground = i < ground_level_Z
ground.array[:, :, underground] = 1
ground.rgb = [0.1,0.5,0.1]


agents = []
for i in range(agent_count):
    agent = Agent(
        space_layer = agent_space,
        track_layer=track_layer,
        leave_trace=True,
        ground_layer=ground, 
        walk_on_ground=True)
    
    # agent.pose = [np.random.randint(0, voxel_size,[3])]
    x = np.random.randint(0, voxel_size)
    y = np.random.randint(0, voxel_size)
    agent.pose = [x, y, ground_level_Z]
    agents.append(agent)

for i in range(iterations):
    for agent in agents:
        #follow random pheromones
        random_pheromones = agent.random_pheromones()
        # random_pheromones_2 = agent.random_pheromones()
        choice = random_pheromones
        dir_key = agent.follow_pheromones(choice)
        # print(dir_key) # choice.argmax()

# add layers and layer_colors
c1 = ground.color_array
c2 = agent_space.color_array
c3 = track_layer.color_array

show_layer = ground.array + agent_space.array + track_layer.array
show_layer_colors = np.minimum(c1 + c2 + c3, 1)
# show_layer_colors = c1 + c2 + c3
# show image
f,a = init_fig()
show_voxel(f,a, show_layer, show_layer_colors, save=True)