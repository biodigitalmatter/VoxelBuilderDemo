import matplotlib.pyplot as plt
from datetime import datetime
from numpy import clip
from helpers import convert_array_to_points
from voxelbuilderdemo import IMG_DIR, TIMESTAMP

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