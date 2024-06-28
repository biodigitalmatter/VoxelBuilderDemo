from voxel_builder_library import *
from show_voxel_plt import *


n = 5
space = Layer(voxel_size=n, )
space.empty_array()
agent = Agent()
agent.position = [1,1,1]
set_value_at_index(space.array, agent.position, value=2)
agent.move('left')
set_value_at_index(space.array, agent.position)
# print(space.array)
# move follow_pheromones
pheromes = agent.random_pheromones()
pheromes = np.arange(6)
choice = np.argmax(pheromes)
agent.move(direction_keys[choice])

# update space
set_value_at_index(space.array, agent.position, value=0.5)

agent.move('up')
set_value_at_index(space.array, agent.position, value=0.3)
agent.move('left')
set_value_at_index(space.array, agent.position, value = 0.123)
values = agent.get_nb_cell_values_of_layer(space)
print(space.array)
print(values)
choice = np.argmax(values)
print(direction_keys[choice])
f,a = init_fig()
show_voxel(f,a, space.array)