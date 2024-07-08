# Other helper functions
from compas.geometry import Pointcloud
import numpy as np
import json


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

def convert_array_to_compas_pointcloud_sorted(ptcloud_array, order_keys = []):
    a = ptcloud_array
    indicies = np.indices(a.shape)
    pt_location = np.logical_not(a == 0)
    coordinates = []
    for i in range(3):
        c = indicies[i][pt_location]
        coordinates.append(c)
    pts = np.vstack(coordinates).transpose()
    sorting_keys = list(a[pt_location])
    pts.sort(sorting_keys)
    ptcloud = Pointcloud(points = pts)
    return ptcloud

def convert_array_to_points(a, list_output = False):
    indicies = np.indices(a.shape)
    pt_location = np.logical_not(a == 0)
    coordinates = []
    for i in range(3):
        c = indicies[i][pt_location]
        coordinates.append(c)
    if list_output:
        pts = np.vstack(coordinates).transpose().tolist()
    else:
        pts = np.vstack(coordinates).transpose()
    return pts

def save_array(array, filename):
    data = array.tolist()
    with open(filename, 'w') as file:
        json.dump(data, file)

def save_ptcloud(ptcloud, filename):
    with open(filename, 'w') as file:
        ptcloud.to_json(file, True)

# # TEST

# array = np.zeros([4,4,4])
# array[:,:2,:1] = 1
# print(array)
# array.tofile('scr/data/test_save_as_file.json')

# # save compas.Pointcloud
# ptcloud = convert_array_to_compas_pointcloud(array)
# filename_ptcloud = 'scr/data/compas_ptclouds/test_compas_point_cloud.json'
# save_ptcloud(ptcloud, filename_ptcloud)
# # read
# with open(filename_ptcloud, 'r') as file:
#     # ptcloud_imported = json.load(file)
#     pointcloud_imported = Pointcloud.from_json(file)
# print('imported Pointcloud object:\n', pointcloud_imported)

# # save point array
# pt_array = convert_array_to_points(array)
# filename_pt_array = 'scr/data/test_save_point_array.json'
# save_array(pt_array, filename_pt_array)
# # read
# with open(filename_pt_array, 'r') as file:
#     point_list_imported = json.load(file)
# print('imported point list:\n', point_list_imported)

# # save pure numpy array:
# filename_np_array = 'scr/data/test_np_array.json'
# save_array(array, filename_np_array)
# # read
# with open(filename_np_array, 'r') as file:
#     array_imported = json.load(file)
# print('imported numpy array:\n', array_imported)

    
