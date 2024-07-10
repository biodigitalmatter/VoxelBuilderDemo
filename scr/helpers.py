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

def convert_array_to_compas_pointcloud_sorted(ptcloud_array):
    a = ptcloud_array
    indicies = np.indices(a.shape)
    pt_location = np.logical_not(a == 0)
    coordinates = []
    for i in range(3):
        c = indicies[i][pt_location]
        coordinates.append(c)
    pts = np.vstack(coordinates).transpose()
    values = list(a[pt_location])
    ptcloud = Pointcloud(points = pts)
    return ptcloud, values

def convert_array_to_pts_sorted(ptcloud_array, return_values = True, multiply = 1):
    a = ptcloud_array
    indicies = np.indices(a.shape)
    pt_location = np.logical_not(a == 0)
    coordinates = []
    for i in range(3):
        c = indicies[i][pt_location]
        coordinates.append(c)

    pts = np.vstack(coordinates).transpose().tolist()
    values = a[pt_location].tolist()
    # sort:
    pts = pts
    values = values

    # Pair the elements using zip
    paired_lists = list(zip(values, pts))

    # Sort the paired lists based on the first element of the pairs (values values)
    sorted_paired_lists = sorted(paired_lists, key=lambda x: x[0])

    # Extract the sorted nested list
    
    if return_values:
        sortedpts = [element[1] for element in sorted_paired_lists]
        values = [element[0] * multiply for element in sorted_paired_lists]
        list_to_dump = {'pt_list' : sortedpts, 'values' : values}
    else:
        list_to_dump = {'pt_list' : sortedpts, 'values' : []}
    return list_to_dump

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
