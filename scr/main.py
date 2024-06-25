# test functions

import voxel_builder_library as builder
import show_voxel_plt as view
import numpy as np

n = 15

smells = builder.Layer('air', voxel_size = n, diffusion_strength= 1 / 20)
smells.rgb = [1,1,1]
# smells.random(add = -0.95, crop=True, strech=1)
a = smells.zeros()
a[2][4][6] = 1
smells.array = a
view.show_voxel(smells.array, smells.colors)
for i in range(10):
    smells.diffuse(repeat=1)
    view.show_voxel(smells.array, smells.colors)
print('done\n',smells.__repr__)