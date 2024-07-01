import matplotlib.pyplot as plt
from datetime import datetime
global timestamp_now
timestamp = datetime.now()
timestamp_now = timestamp.strftime("%y%m%d_%H%M%S")

def init_fig(title = 'img', suffix = '', bottom_line = ''):
    fig = plt.figure(figsize = [4, 4], dpi = 200)
    ax = fig.add_subplot(projection='3d')
    ax.set_proj_type('persp', focal_length = 0.4)

    # style    
    fig.suptitle('%s_%s_%s.png' %(title, timestamp_now, suffix), fontsize = 5)
    fig.text(0,0, s = bottom_line, fontsize = 3.4, verticalalignment = 'baseline' )
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    return fig, ax

def show_voxel(fig, ax, voxel_fill_3D, colors_4D = None, show = True, save = False, title = 'img', suffix = ''):
    # plot voxels
    ax.voxels(voxel_fill_3D, facecolors = colors_4D)

    if save:
        plt.savefig('img/%s_%s_%s.png' %(title, timestamp_now, suffix), bbox_inches='tight', dpi = 200)
        print('saved')

    if show:
        plt.show()


def show(fig, ax, layer, save_img = True, show_img = True,  title = 'voxels_test_smells', suffix = '', note = '', discretize_gradient = True):
    if discretize_gradient: layer.grade()
    layer.calculate_color_array()
    
    show_voxel(fig, ax, layer.array, layer.color_array, save=save_img, show = show_img, title=title, suffix = suffix)


# # animation template

# from matplotlib import animation
# from matplotlib import pyplot as plt

# def update():
#     "generate next plot"
#     pass

# def animate(frame):
#     update()

# figure = None

# anim = animation.FuncAnimation(figure, animate, frames = 50, interval = 50)
# # anim.save("img/gif/test.gif")
# plt.show()