import matplotlib.pyplot as plt
from datetime import datetime
from numpy import maximum, minimum, clip
from helpers import convert_array_to_points
from voxelbuilderdemo import IMG_DIR

global timestamp_now
timestamp = datetime.now()
timestamp_now = timestamp.strftime("%y%m%d_%H%M%S")


def init_fig(title="img", suffix="", bottom_line=""):
    fig = plt.figure(figsize=[4, 4], dpi=200)
    ax = fig.add_subplot(projection="3d")
    ax.set_proj_type("persp", focal_length=0.4)

    # style
    fig.suptitle("%s_%s_%s.png" % (title, timestamp_now, suffix), fontsize=5)
    fig.text(0, 0, s=bottom_line, fontsize=3.4, verticalalignment="baseline")

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    return fig, ax


def show_voxel(
    fig,
    ax,
    voxel_fill_3D,
    colors_4D=None,
    show=True,
    save=False,
    title="img",
    suffix="",
):
    # plot voxels
    try:
        colors_4D = minimum(colors_4D, 1)
        colors_4D = maximum(colors_4D, 0)
    except:
        pass
    # print('show_colors:')
    # print(colors_4D)
    ax.voxels(voxel_fill_3D, facecolors=colors_4D)

    if save:
        plt.savefig(
            f"{IMG_DIR}/{title}_{timestamp_now}_{suffix}.png",
            bbox_inches="tight",
            dpi=200,
        )
        print("saved")

    if show:
        plt.show()


def show_scatter(fig, ax, arrays_to_show):
    # fig = plt.figure()
    # axes = plt.axes(xlim=(0, scale), ylim =  (0, scale), zlim = (0, scale), projection = '3d')
    # axes.set_xticks([])
    # axes.set_yticks([])
    # axes.set_zticks([])
    for array in arrays_to_show:
        p = array.transpose()
        ax.scatter(p[0, :], p[1, :], p[2, :], marker="s", s=2)


def show(
    fig,
    ax,
    layer,
    save_img=True,
    show_img=True,
    title="voxels_test_smells",
    suffix="",
    note="",
    discretize_gradient=True,
):
    if discretize_gradient:
        layer.grade()
    layer.calculate_color_array()

    show_voxel(
        fig,
        ax,
        layer.array,
        layer.color_array,
        save=save_img,
        show=show_img,
        title=title,
        suffix=suffix,
    )


def plot_voxels_2(ax, voxel_grids, colors, edgecolor=None, clear_ax=True, trim_below = 1):
    if clear_ax:
        ax.clear()
    for i in range(len(voxel_grids)):
        a1 = voxel_grids[i].copy()
        a1 = a1[:, :, trim_below:]
        ax.voxels(a1, facecolors=colors[i], edgecolor=edgecolor)
    ax.set_xlim(0, voxel_grids[0].shape[0])
    ax.set_ylim(0, voxel_grids[0].shape[1])
    ax.set_zlim(0, voxel_grids[0].shape[2])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    ax.set_box_aspect([1, 1, 1])  # Aspect ratio is 1:1:1


def plot_voxel_2(ax, voxel_grid, color="blue"):
    ax.clear()
    ax.voxels(voxel_grid, facecolors=color, edgecolor="k")
    ax.set_xlim(0, voxel_grid.shape[0])
    ax.set_ylim(0, voxel_grid.shape[1])
    ax.set_zlim(0, voxel_grid.shape[2])
    ax.set_box_aspect([1, 1, 1])  # Aspect ratio is 1:1:1
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])


def show_voxel_2(voxel_grid, color="red"):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    # ax.clear()
    ax.voxels(voxel_grid, facecolors=color, edgecolor="k")
    ax.set_xlim(0, voxel_grid.shape[0])
    ax.set_ylim(0, voxel_grid.shape[1])
    ax.set_zlim(0, voxel_grid.shape[2])
    ax.set_box_aspect([1, 1, 1])  # Aspect ratio is 1:1:1
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    plt.show()


def show_voxels_2(ax, voxel_grids, colors, edgecolor="k"):
    ax.clear()
    for i in range(len(voxel_grids)):
        ax.voxels(voxel_grids[i], facecolors=colors[i], edgecolor="k")
    ax.set_xlim(0, voxel_grids[0].shape[0])
    ax.set_ylim(0, voxel_grids[0].shape[1])
    ax.set_zlim(0, voxel_grids[0].shape[2])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    plt.show()


def scatter_layers(axes, layers, clear=False, scale=10, trim_below=0, color_4D=False):
    # axes.clear()
    if clear:
        axes.clear()
        axes = plt.axes(
            xlim=(0, scale), ylim=(0, scale), zlim=(0, scale), projection="3d"
        )
        axes.set_xticks([])
        axes.set_yticks([])
        axes.set_zticks([])
    for layer in layers:
        if color_4D:
            facecolor = layer.color_array[:,:,:,trim_below:]
            facecolor = clip(facecolor, 0, 1)
        else:
            facecolor = layer.rgb
        # scatter plot
        a1 = layer.array.copy()
        pt_array = convert_array_to_points(a1[:, :, trim_below:], False)
        p = pt_array.transpose()
        axes.scatter(p[0, :], p[1, :], p[2, :], marker="s", s=1, facecolor=facecolor)


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
