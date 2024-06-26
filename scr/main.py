# test functions

import voxel_builder_library as designer
import show_voxel_plt as view
import numpy as np

n = 30
iter = 20
show_img = True
save_img = True

smells = designer.Layer()
smells.name = 'smells'
smells.voxel_size = n
smells.diffusion_ratio = 1/7
smells.decay_ratio = 0
smells.decay_random_factor = 0
smells.diffusion_random_factor = 0.3
smells.gradient_resolution = 20000
smells.rgb = [1,1,1]

# initiate random drops
smells.empty_array()
smells.array[0][int(n/3)][0] = 1
# for _ in range(2):
#     i, j, k = np.random.randint(0, n -1, size = 3)
#     smells.array[i][j][k] = 1 - np.random.random(1) * 0.2
for i in range(iter):
    # decay
    smells.decay()
    # diffuse
    smells.diffuse(limit_by_Hirsh=False, reintroduce_on_the_other_end=False)
    # # add new drops
    # i, j, k = np.random.randint(0, n -1, size = 3)
    # smells.array[i][j][k] = np.random.random(1) + 0.5

# discretize gradient
smells.grade()

# show result and save image
print(smells)
print(smells.array[0][0][0], smells.array[0][0][1], smells.array[1][0][1])
bottomline = smells.__str__()
smells.calculate_color_array()
view.show_voxel(smells.array, smells.color_array, save=save_img, show = show_img, title='voxels_test_smells', suffix = 'n-%s_iter-%s_diffusion_validation' %(smells._n, iter), bottom_line = bottomline)

print('done')
