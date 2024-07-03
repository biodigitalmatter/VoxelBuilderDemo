# Other helper functions
from compas.geometry import Pointcloud
import numpy as np

array = np.zeros([4,4,4])
array[:,:2,:1] = 1
print(array)

def convert_array_to_compas_pointcloud(ptcloud_array, order = 'xyz'):
    a = ptcloud_array
    indicies = np.indices(a.shape)
    pt_location = np.logical_not(a == 0)
    coordinates = []
    for i in range(3):
        c = indicies[i][pt_location]
        coordinates.append(c)
    pts = np.vstack(coordinates).transpose()
    ptcloud = Pointcloud(points = pts)
    return ptcloud

ptcloud = convert_array_to_compas_pointcloud(array)
print(ptcloud)
file = 'test_compas_point_cloud.json'
ptcloud.to_json(file, True)


# Pointcloud.from_json(file)