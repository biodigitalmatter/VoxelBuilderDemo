from voxel_builder_library import *
from show_voxel_plt import *


voxel_size = 60
agent_count = 2
iterations = 25

space = Layer(voxel_size=voxel_size)

agents = []
for i in range(agent_count):
    agent = Agent(space_layer = space, trace=True)
    agent.pose = [np.random.randint(0, voxel_size,[3])]
    agents.append(agent)
for i in range(iterations):
    for agent in agents:
        #follow random pheromones
        random_pheromones = agent.random_pheromones()
        # random_pheromones_2 = agent.random_pheromones()
        choice = random_pheromones
        dir_key = agent.follow_pheromones(choice)
        print(dir_key) # choice.argmax()


# show image
f,a = init_fig()
show_voxel(f,a, space.array)