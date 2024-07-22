
import os
from compas.colors import Color
from compas.geometry import Pointcloud, Capsule, Box, Frame, Line, Sphere
from compas.geometry import Transformation, Translation, matrix_from_frame_to_frame, Scale, matrix_from_scale_factors

from compas_view2.app import App

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
radius = 1
folder_path = os.path.join(os.getcwd(), 'data/json/compas_pointclouds')

# LOAD JSON
file = get_nth_newest_file_in_folder(folder_path, Nth)
print(file)
try: 
    os.path.isfile(file) # open file
    ptcloud = Pointcloud.from_json(file)
    # network = Network.from_json(file)
    pts = ptcloud.points
    print(len(pts))   

except Exception as e:
    print(f"Error: {e}")

# # CREATE BASIC SHAPE - BOX
world_xy = Frame.worldXY()
shape = Box(world_xy, radius, radius, radius)
# shape = Sphere([0,0,0], radius)

# # CREATE BASIC SHAPE - CAPSULE
# ratio = 4
# # pt2 = [] + [0,0, radius / 5]
# # line = Line([0,0,0], [0,0,radius])
# # shape = Capsule(line, radius)

# m = matrix_from_scale_factors([1,1, 0.5])
# scale_v = Transformation(m)
# shape.transform(scale_v)


# SETUP VIEWER
viewer = App(width=600, height=600)
viewer.view.camera.rx = -60
viewer.view.camera.rz = 30
viewer.view.camera.ty = -2
viewer.view.camera.distance = 20

viewer.add(ptcloud)

# PLace and add objects at locations
for pt in pts:
    frame_to = Frame(pt, [1,0,0], [0,1,0])
    shape2 = shape.copy()
    move = Transformation(matrix_from_frame_to_frame(world_xy, frame_to))
    shape2.transform(move)
    # objs.append(shape2)
    viewer.add(shape2, opacity=1)
    # green = Color.green()
    # green = Color(135/255, 150/255, 100/255)

print('show starts')
viewer.show()



print('show done')

