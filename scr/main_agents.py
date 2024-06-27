from voxel_builder_library import *
from show_voxel_plt import *


n = 5
space = Layer(voxel_size=n, )
space.empty_array()
agent = Agent()
agent.position = [1,1,1]
agent.move('up')
space.array = set_value_at_index(space.array, agent.position)
agent.move

f,a = init_fig()
show_voxel(f,a, space.array)