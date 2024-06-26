# test functions

import voxel_builder_library as builder
import show_voxel_plt as view
import numpy as np

n = 60
iter = 20
save_img = True

smells = builder.Layer()
smells.name = 'smells'
smells.voxel_size = n
smells.diffusion_ratio = 1/7
smells.decay_ratio = 0.01
smells.decay_random_factor = 0
smells.diffusion_random_factor = 0
smells.gradient_resolution = 100

# initiate random drops
smells.empty_array()
print(smells.array.shape)

for _ in range(1):
    i, j, k = np.random.randint(0, n -1, size = 3)
    smells.array[i][j][k] = np.random.random(1) + 0.5
for i in range(iter):
    # decay
    smells.decay()
    # diffuse
    smells.diffuse()
    # add new drops
    i, j, k = np.random.randint(0, n -1, size = 3)
    smells.array[i][j][k] = np.random.random(1) + 0.5

# discretize gradient
smells.grade()

# show result and save image
view.show_voxel(smells.array, smells.color_array, save=save_img, title='voxels_test_smells', suffix = 'n-%s_iter-%s' %(smells._n, iter), bottom_line = smells.__repr__)

print('done')