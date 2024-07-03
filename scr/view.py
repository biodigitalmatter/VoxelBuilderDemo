
import os
from compas.colors import Color
from compas.geometry import Pointcloud

def get_newest_file_in_folder(folder_path):
    try:
        # Get a list of files in the folder
        files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)]
        # print(files)
        # Sort the files by change time (modification time) in descending order
        # files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        print('files in folder:')
        print(files)
        # Return the newest file
        if files:
            return files[0]
        else:
            print("Folder is empty.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_nth_newest_file_in_folder(folder_path, n):
    try:
        # Get a list of files in the folder
        files = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path)]

        # Sort the files by change time (modification time) in descending order
        files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

        # Return the newest file
        if files:
            return files[min(n, len(files))]
        else:
            print("Folder is empty.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

# params
Nth = 0
show = True
radius = 0.25
folder_path = os.path.join(os.getcwd(), 'scr/data/compas_ptclouds')

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
        viewer.view.camera.rz = 30
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

