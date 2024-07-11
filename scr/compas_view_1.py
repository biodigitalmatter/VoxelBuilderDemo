
import os
from compas.colors import Color
from compas.geometry import Pointcloud
from helpers import *

import argparse
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
    Nth = 0


# params
# Nth = 0
show = True
radius = 1
folder_path = os.path.join(os.getcwd(), 'data/json/compas_pointclouds')

file = get_nth_newest_file_in_folder(folder_path, Nth)

try: 
    os.path.isfile(file) # open file
    ptcloud = Pointcloud.from_json(file)
    # network = Network.from_json(file)
    
    # =============================================================================
    if show: # SHOW network
        from compas_view2.app import App

        viewer = App(width=600, height=600)
        viewer.view.camera.rx = -60
        viewer.view.camera.rz = 100
        viewer.view.camera.ty = -2
        viewer.view.camera.distance = 20

        viewer.add(ptcloud)

        green = Color.green()
        green = Color(135/255, 150/255, 100/255)
        print('show starts')
        viewer.show()

except Exception as e:
    print(f"Error: {e}")

print('show done')

