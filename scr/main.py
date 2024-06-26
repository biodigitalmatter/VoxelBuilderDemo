# test functions

import voxel_builder_library as builder
import show_voxel_plt as view
import numpy as np

n = 60

smells = builder.Layer('air', voxel_size = n, diffusion_strength= 1/7 , decay = 0.01)
smells.rgb = [1,1,0]
smells.rgb = [1,0.998,0.999]
# smells.random(add = -0.95, crop=True, strech=1)
a = smells.zeros()
# a[4][4][4] = 1
for _ in range(5):
    i, j, k = np.random.randint(0, n -1, size = 3)
    a[i][j][k] = np.random.random(1) + 0.5
smells.array = a
# view.show_voxel(smells.array, smells.colors)

for i in range(55):
    smells.decay_proportional(randomize = True)
    smells.diffuse2(repeat=1, randomize=True, factor = 0)
    i, j, k = np.random.randint(0, n -1, size = 3)
    a[i][j][k] = np.random.random(1) + 0.5


a = smells.array
grading = 500
a = np.int64(a * grading) / grading
smells.array = a
name = 'grade-500'
view.show_voxel(smells.array, smells.colors, save=True, No = name)

print('done')
# print('done\n',smells.__repr__)