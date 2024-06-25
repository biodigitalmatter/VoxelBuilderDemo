# test functions

import voxel_builder_library as builder
import show_voxel_plt as view
import numpy as np

n = 9

smells = builder.Layer('air', voxel_size = n, diffusion_strength= 1/36 , decay = 0.8)
smells.rgb = [1,0.998,0.999]
# smells.random(add = -0.95, crop=True, strech=1)
a = smells.zeros()
# a[4][4][4] = 1
a[0][0][0] = 1

smells.array = a
view.show_voxel(smells.array, smells.colors)
for i in range(5):
    smells.decay_proportional(randomize = True)
    # smells.decay_absolute()
    smells.diffuse2(repeat=2)
    
    
    view.show_voxel(smells.array, smells.colors)
# print(np.amin(smells.array), np.amax(smells.array) )
# print(smells.array)
print('done')
# print('done\n',smells.__repr__)