from show_voxel_plt import *
from helpers import *
import argparse
import json
import numpy as np


def load_json_w_parse(n=0):
    # Create the parser
    parser = argparse.ArgumentParser(description="provide int variable: i.")
    # Add an argument
    parser.add_argument("nth", type=int, help="i : nth json to open")
    try:
        # Parse the command-line arguments
        args = parser.parse_args()
        Nth = int(args.nth)
    except Exception as e:
        # print()
        Nth = n

    return Nth


def show_scatter_main(fig, axes, array, scale=0):
    """voxel_like array masked"""
    # if scale != 0:
    #     axes = plt.axes(xlim=(0, scale), ylim =  (0, scale), zlim = (0, scale), projection = '3d')
    axes.set_xticks([])
    axes.set_yticks([])
    axes.set_zticks([])
    p = array.transpose()
    axes.scatter(p[0, :], p[1, :], p[2, :], marker="s", s=2)


def show_voxel_main(
    fig, axes, voxel_fill_3D, show=True, save=False, title="img", suffix=""
):
    # plot voxels

    # print('show_colors:')
    # print(colors_4D)
    x, y, z = voxel_fill_3D.shape
    axes = plt.axes(xlim=(0, x), ylim=(0, y), zlim=(0, z), projection="3d")
    axes.voxels(voxel_fill_3D)
    axes.set_xticks([])
    axes.set_yticks([])
    axes.set_zticks([])

    if save:
        plt.savefig(
            f"{IMG_DIR}/{title}_{timestamp_now}_{suffix}.png",
            bbox_inches="tight",
            dpi=200,
        )
        print("saved")

    if show:
        plt.show()


def voxel_array_from_pt_list(points):
    """input:
    points: numpy array.shape = (n,3)
    return 3D voxel_like array"""
    max = np.max(points) + 1
    grid_shape = (max, max, max)

    # Create a 3D boolean array initialized to False
    voxel_grid = np.zeros(grid_shape, dtype=bool)

    # Set the corresponding voxels to True
    for point in points:
        voxel_grid[point[0], point[1], point[2]] = True

    return voxel_grid


if __name__ == "__main__":
    try:
        n = load_json_w_parse(0)
    except:
        n = 0
    n = 0
    folder_path = "data/json/points_values"

    filename = get_nth_newest_file_in_folder(folder_path, n)

    with open(filename, "r") as fp:
        d = json.load(fp)

    sorted_pts = d["pt_list"]

    points = np.asarray(sorted_pts)
    voxel_array = voxel_array_from_pt_list(points)

    fig, axes = init_fig()

    show_voxel_main(fig, axes, voxel_array)

    plt.show()
