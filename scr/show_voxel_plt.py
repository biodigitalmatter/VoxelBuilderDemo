import matplotlib.pyplot as plt
from datetime import datetime
global timestamp_now
timestamp = datetime.now()
timestamp_now = timestamp.strftime("%y%m%d_%H%M%S")
def show_voxel(voxel_fill_3D, colors_4D = None, show = True, save = False, title = 'img', suffix = '', bottom_line = ''):
    # ################## visualise
    # # and plot everything
    fig = plt.figure(figsize = [4, 4], dpi = 200)
    ax = fig.add_subplot(projection='3d')
    ax.set_proj_type('persp', focal_length = 0.4)

    # voxels
    ax.voxels(voxel_fill_3D, facecolors = colors_4D)

    # style    
    fig.suptitle('%s_%s_%s.png' %(title, timestamp_now, suffix), fontsize = 5)
    fig.text(0,2, s = str(bottom_line), fontsize = 2.5)
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    # save
    # save = False
    # title = 'img'
    # No = 1
    if save:
        plt.savefig('img/%s_%s_%s.png' %(title, timestamp_now, suffix), bbox_inches='tight', dpi = 200)
        print('saved')

    if show:
        plt.show()

