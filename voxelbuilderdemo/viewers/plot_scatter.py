from helpers import *
import argparse
import json
import numpy as np
from voxelbuilderdemo import IMG_DIR, TIMESTAMP
from datetime import datetime
import matplotlib.pyplot as plt

""" 'standalone' point_scatter plotter to show json pointcloud
"""

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

def init_fig(title="img", suffix="", bottom_line=""):
    fig = plt.figure(figsize=[4, 4], dpi=200)
    ax = fig.add_subplot(projection="3d")
    ax.set_proj_type("persp", focal_length=0.4)

    # style
    fig.suptitle("%s_%s_%s.png" % (title, TIMESTAMP, suffix), fontsize=5)
    fig.text(0, 0, s=bottom_line, fontsize=3.4, verticalalignment="baseline")

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    return fig, ax

def show_scatter(fig, ax, arrays_to_show):
    # fig = plt.figure()
    # axes = plt.axes(xlim=(0, scale), ylim =  (0, scale), zlim = (0, scale), projection = '3d')
    # axes.set_xticks([])
    # axes.set_yticks([])
    # axes.set_zticks([])
    for array in arrays_to_show:
        p = array.transpose()
        ax.scatter(p[0, :], p[1, :], p[2, :], marker="s", s=2)

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
