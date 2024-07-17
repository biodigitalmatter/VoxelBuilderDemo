# test_main_1.py
from class_agent import *
from class_layer import *


# LAYERS

voxel_size = 10
### LAYERS OF THE ENVIRONMENT
rgb_sky = [29, 77, 222]
rgb_agents = [34,116,240]
rgb_clay_moisture = [167, 217, 213]
rgb_air_moisture = [200, 204, 219]
rgb_ground = [207, 179, 171]

ground = Layer(voxel_size=voxel_size, name='ground', rgb = [i/255 for i in rgb_ground])
agent_space = Layer('agent_space', voxel_size = voxel_size, rgb = [i/255 for i in rgb_agents])
queen_bee_space = Layer(voxel_size=voxel_size, rgb=[203/255, 21/255, 207/255])
queen_bee_pheromon = Layer('queen_bee_pheromon', voxel_size=voxel_size, rgb = [i/255 for i in rgb_sky])

### AGENTS



### CREATE ENVIRONMENT
# make ground
# ground.array += make_solid_box_z(voxel_size, 1)