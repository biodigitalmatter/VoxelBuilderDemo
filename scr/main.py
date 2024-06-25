# test functions

import voxel_builder_library as builder
import show_voxel_plt as view
import numpy as np

n = 7

smells = builder.Layer('air', voxel_size = n, diffusion_strength= 1/36 , decay = 0.8, absolute_decay= 0.001)
smells.rgb = [0.8, 0.1, 0.2]
# smells.random(add = -0.95, crop=True, strech=1)
a = smells.zeros()
a[2][4][6] = 1

smells.array = a
view.show_voxel(smells.array, smells.colors)
for i in range(8):
    smells.decay_propotional()
    smells.decay_absolute()
    smells.diffuse()
    
    
    view.show_voxel(smells.array, smells.colors)
print(np.amin(smells.array), np.amax(smells.array) )
print(smells.array)
print('done\n',smells.__repr__)