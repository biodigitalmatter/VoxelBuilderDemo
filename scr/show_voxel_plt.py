import matplotlib.pyplot as plt

def show_voxel(voxel_fill_3D, colors_4D, show = True, save = False, title = 'img', No = 1):
    # ################## visualise
    # # and plot everything
    fig = plt.figure(figsize = [4, 4], dpi = 200)
    ax = fig.add_subplot(projection='3d')
    ax.set_proj_type('persp', focal_length = 0.4)

    # voxels
    ax.voxels(voxel_fill_3D, facecolors = colors_4D)
    
    # style
    filename = __file__
    fig.suptitle("%s_%s-%ds" %(filename, title, No ), fontsize = 5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    # save
    save = False
    title = 'img'
    No = 1
    if save:
        plt.savefig('img/%s-%s.png' %(title, No), bbox_inches='tight', dpi = 200)
        print('saved')

    if show:
        plt.show()

