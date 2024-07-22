from show_voxel_plt import *
from helpers import *
import argparse
import json
import numpy as np

def load_json_w_parse(n = 0):
    # Create the parser
    parser = argparse.ArgumentParser(description="provide int variable: i.")
    # Add an argument
    parser.add_argument('nth', type=int, help='i : nth json to open')
    try:
        # Parse the command-line arguments
        args = parser.parse_args()
        Nth = int(args.nth)
    except Exception as e:
        # print()
        Nth = n

    
    return Nth

def show_scatter_main(fig, axes, array, scale = 0):
    """voxel_like array masked"""
    if scale != 0:
        axes = plt.axes(xlim=(0, scale), ylim =  (0, scale), zlim = (0, scale), projection = '3d')
    axes.set_xticks([])
    axes.set_yticks([])
    axes.set_zticks([])
    p = array.transpose()
    axes.scatter(p[0, :], p[1, :], p[2, :], marker = 's', s = 2)


if __name__ == '__main__':
    try:
        n = load_json_w_parse(0)
    except:
        n = 0

    folder_path = 'data/json/points_values'

    filename = get_nth_newest_file_in_folder(folder_path, n)

    with open(filename, 'r') as fp:
        d = json.load(fp)

    sorted_pts = d['pt_list']

    layer = np.asarray(sorted_pts)
    # print(layer)

    fig, ax = init_fig()

    layers = [layer]
    show_scatter(fig, ax, layers)
    # s = np.amax(layer)
    # show_scatter_main(fig, ax, layer, 0)


    plt.show()
