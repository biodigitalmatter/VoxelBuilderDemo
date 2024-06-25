# test functions

import voxel_builder_library as builder
import show_voxel_plt as view
import numpy as np

n = 9

smells = builder.Layer('air', voxel_size = n, diffusion_strength= 1/7 , decay = 0.0001, voxel_visibility=[0.2, 1])
smells.rgb = [1,0.998,0.999]
# smells.random(add = -0.95, crop=True, strech=1)
a = smells.zeros()
# a[4][4][4] = 1
a[0][0][0] = 1

smells.array = a
view.show_voxel(smells.array, smells.colors)
for i in range(5):
    smells.decay_proportional(randomize = False)
    smells.diffuse2(repeat=1, randomize=False, factor = 0)
    view.show_voxel(smells.array, smells.colors)

print('done')
# print('done\n',smells.__repr__)