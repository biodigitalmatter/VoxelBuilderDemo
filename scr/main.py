# test functions

import voxel_builder_library as designer
import show_voxel_plt as view
import numpy as np

# SETTINGS #
n = 30
iter = 5
note = 'test_animation'

show_result = True
save_img = False

show_animation = True
show_nth = 1
save_anim = False

# CREATE OBJECTS #
smells = designer.Layer()
smells.name = 'smells'
smells.voxel_size = n
smells.diffusion_ratio = 1/36
smells.decay_ratio = 0
smells.decay_random_factor = 0
smells.diffusion_random_factor = 0
smells.gradient_resolution = 0
smells.rgb = [1,1,1]

# SIMULATION SETUP #
smells.empty_array()

# add one drop
smells.array[n-1][int(n/3)][0] = 1
# order = ('x','y','z') #!!!???
# add random drops
# for _ in range(2):
#     i, j, k = np.random.randint(0, n -1, size = 3)
#     smells.array[i][j][k] = 1 - np.random.random(1) * 0.2

# RUN #
def run(loop_count):
    for _ in range(loop_count):
        smells.iterate()

# SHOW #
if show_result and not show_animation:
    # generate the result
    run(iter)
    print('voxel_done')
    # initiate figure
    fig, ax = view.init_fig(
        suffix = 'n-%s_iter-%s_%s' %(smells._n, iter, note),
        bottom_line = smells.__str__()
    )
    # show result plot
    view.show(fig, ax, smells)

    # print(smells)
    # print(smells.array[0][0][0], smells.array[0][0][1], smells.array[1][0][1])
    print('plot_done')

# ANIMATION
if show_result and show_animation:
    from matplotlib import animation
    from matplotlib import pyplot as plt

    # initiate figure
    fig, ax = view.init_fig(
        suffix = 'n-%s_iter-%s_%s' %(smells._n, iter, note),
        bottom_line = smells.__str__()
    )

    # animation function

    def animate(frame):
        run(1)
        if animate.counter % show_nth == 0:
            view.show(fig, ax, smells, save_img=False, show_img=False)
        animate.counter += 1

    # run animation
    animate.counter = 0
    anim = animation.FuncAnimation(fig, animate, frames = 50, interval = 50)
    if save_anim:
        anim.save("img/gif/test.gif")
    plt.show()
