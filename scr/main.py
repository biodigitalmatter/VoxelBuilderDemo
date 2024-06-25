# test functions

import voxel_builder_library as builder
import show_voxel_plt as view
import numpy as np

n = 5

smells = builder.Layer('air', voxel_size = n)
smells.rgb = [0,1,0.2]
smells.random(add = -0.9, crop=True, strech=10)

# print('array')
# print(smells.array)
# colors = smells.colors
# print('colors')
# print(colors)
# print('bounds', np.max(colors), np.min(colors))

view.show_voxel(smells.array, smells.colors)