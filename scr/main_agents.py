from voxel_builder_library import *
from show_voxel_plt import *


voxel_size = 40
agent_count = 2
iterations = 25

agent_space = Layer(voxel_size=voxel_size, rgb=[1,0,0])

# create ground:
ground = Layer(voxel_size=voxel_size)
i = np.arange(voxel_size)
underground = i < 2
ground.array[underground, :, :] = 1
ground.rgb = [0, 0.7, 0.2]


agents = []
for i in range(agent_count):
    agent = Agent(
        space_layer = agent_space, leave_trace=True,
        ground_layer=ground, walk_on_ground=True)
    # agent.pose = [np.random.randint(0, voxel_size,[3])]
    x = np.random.randint(0, voxel_size)
    y = np.random.randint(0, voxel_size)
    agent.pose = [2, y, x]
    agents.append(agent)
for i in range(iterations):
    for agent in agents:
        #follow random pheromones
        random_pheromones = agent.random_pheromones()
        # random_pheromones_2 = agent.random_pheromones()
        choice = random_pheromones
        dir_key = agent.follow_pheromones(choice)
        print(dir_key) # choice.argmax()

# add layers and layer_colors
c1 = ground.color_array
# air = ground == 0
c2 = agent_space.color_array

show_layer = ground.array + agent_space.array
show_layer_colors = c1 + c2

# show image
f,a = init_fig()
show_voxel(f,a, show_layer, show_layer_colors, save=True)