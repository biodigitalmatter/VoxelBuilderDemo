# test functions

import voxel_builder_library as designer
import show_voxel_plt as view
import numpy as np

n = 30
iter = 20
show_result = True
show_animation = False
save_img = False
note = 'decay'

smells = designer.Layer()
smells.name = 'smells'
smells.voxel_size = n
smells.diffusion_ratio = 1/36
smells.decay_ratio = 0
smells.decay_random_factor = 0
smells.diffusion_random_factor = 0
smells.gradient_resolution = 0
smells.rgb = [1,1,1]

# SETUP #
smells.empty_array()
# add one drop
smells.array[0][int(n/3)][0] = 1
# add random drops
# for _ in range(2):
#     i, j, k = np.random.randint(0, n -1, size = 3)
#     smells.array[i][j][k] = 1 - np.random.random(1) * 0.2


# RUN #
def run(iter):
    for i in range(iter):
        smells.iterate()

# SHOW #
if show_result and not show_animation:
    fig, ax = view.init_fig(
        suffix = 'n-%s_iter-%s_%s' %(smells._n, iter, note),
        bottom_line = smells.__str__()
    )
    view.show(fig, ax, smells)
    # print(smells)
    # print(smells.array[0][0][0], smells.array[0][0][1], smells.array[1][0][1])
    print('done')

# ANIMATION

# from matplotlib import animation
# from matplotlib import pyplot as plt

# def update():
#     "generate next plot"
#     pass

# def animate(frame):
#     run(1)

# anim = animation.FuncAnimation(figure, animate, frames = 50, interval = 50)
# # anim.save("img/gif/test.gif")
# plt.show()
