from voxel_builder_library import *
from show_voxel_plt import *


voxel_size = 6
agent_count = 2
iterations = 4

space = Layer(voxel_size=voxel_size)

agents = []
for i in range(agent_count):
    agent = Agent(space_layer = space, auto_update=True)
    agents.append(agent)
for i in range(iterations):
    for agent in agents:
        agent.pose = [np.random.randint(0,5,[3])]
        #follow random pheromones
        random_pheromones = agent.random_pheromones()
        random_pheromones_2 = agent.random_pheromones()
        choice = random_pheromones + random_pheromones_2
        dir_key = agent.follow_pheromones(choice)
        # print(dir_key) # choice.argmax()


# show image
f,a = init_fig()
show_voxel(f,a, space.array)