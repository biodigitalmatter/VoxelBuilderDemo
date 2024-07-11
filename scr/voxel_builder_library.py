import numpy as np
from math_functions import *

def create_zero_array(n):
    # create voxel-like array
    a = np.zeros(n ** 3)  # 3 dimensional numpy array representing voxel voxel
    a = np.reshape(a, [n, n, n])
    return a

def create_random_array(n):
    # create voxel-like array
    a = np.random.random(n ** 3)
    a = np.reshape(a, [n, n, n])
    return a

def set_value_at_index(layer, index = [0,0,0], value = 1):
    # print('set value at index', index)
    i,j,k = index
    try:
        layer.array[i][j][k] = value
    except Exception as e:
        print('set value error:%s' %e)
    return layer

def get_layer_value_at_index(layer, index = [0,0,0], reintroduce = True):
    # print('get value at index', index)
    if reintroduce:
        index2 = np.mod(index, layer.voxel_size)
    else:
        index2 = index
    i,j,k = index2
    try:
        v = layer.array[i][j][k]
    except:
        v = 0
    return v

def get_cube_array_indices(self_contain = False):
    """list of 26 neighbor cell indicies_list, ordered: top 9 -middle 8 -bottom 9"""
    # horizontal
    f = direction_dict_np['front']
    b = direction_dict_np['back']
    l = direction_dict_np['left']
    r = direction_dict_np['right']
    u = direction_dict_np['up']
    d = direction_dict_np['down']
    # first_story in level:
    story_1 = [ f + l, f, f + r, l, r, b + l, b, b + r]
    story_0 = [i + d for i in story_1]
    story_2 = [i + u for i in story_1]
    if self_contain:
        nbs_w_corners = story_2 + [u] + story_1 + [np.asarray([0,0,0])] + story_0 + [d]
    else:
        nbs_w_corners = story_2 + [u] + story_1 + story_0 + [d]
    return nbs_w_corners

def get_nb_cell_directions_w_edges():
    # horizontal
    f = direction_dict_np['front']
    b = direction_dict_np['back']
    l = direction_dict_np['left']
    r = direction_dict_np['right']
    u = direction_dict_np['up']
    d = direction_dict_np['down']
    # first_story in level:
    story_1 = [f, f + l, f + r, l, r, b, b + l, b + r]
    story_0 = [i + d for i in [f,b,l,r]]
    story_2 = [i + u for i in [f,b,l,r]]
    nbs_w_corners = story_1 + story_0 + story_2 + [u] + [d] + [np.asarray([0,0,0])]
    return nbs_w_corners

def get_nb_cell_directions_w_edges():
    # horizontal
    face_nbs = list(direction_dict_np.values())
    nbs_w_edges = face_nbs + [np.asarray([0,0,0])]
    return nbs_w_edges

def conditional_fill(array, n, condition = '<', value = 0.5, override_self = False):
    """returns new voxel_array with 0,1 values based on condition"""
    if condition == '<':
        mask_inv = array < value
    elif condition == '>':
        mask_inv = array > value
    elif condition == '<=':
        mask_inv = array <= value
    elif condition == '>=':
        mask_inv = array >=  value
    a = create_zero_array(n)
    a[mask_inv] = 0
    if override_self:
        array = a
    return a

def make_solid_box_z(voxel_size, z_max):
    n = voxel_size
    test_i = np.indices((n,n,n))
    z = test_i[2,:,:,:] <= z_max
    d = np.zeros((n,n,n))
    d[z] = 1
    return d

def make_solid_box_xxz(voxel_size, x_min, x_max, z_max):
    n = voxel_size
    test_i = np.indices((n,n,n))
    x1 = test_i[0,:,:,:] >= x_min
    x2 = test_i[0,:,:,:] <= x_max
    z = test_i[2,:,:,:] <= z_max
    d = np.zeros((n,n,n))
    d[x2 & x1 & z] = 1
    return d

def make_solid_box_xxyyzz(voxel_size, x_min, x_max, y_min, y_max, z_min, z_max):
    """boolean box including limits"""
    n = voxel_size
    test_i = np.indices((n,n,n))
    x1 = test_i[0,:,:,:] >= x_min
    x2 = test_i[0,:,:,:] <= x_max
    y1 = test_i[1,:,:,:] >= y_min
    y2 = test_i[1,:,:,:] <= y_max
    z1 = test_i[2,:,:,:] >= z_min
    z2 = test_i[2,:,:,:] <= z_max
    d = np.zeros((n,n,n))
    d[x2 & x1 & y1 & y2 & z1 & z2] = 1
    return d

def get_sub_array(array, offset_radius, center = None, format_values = None):
    """gets sub array around center, in 'offset_radius'
    format values: returns sum '0', avarage '1', or all_values: 'None'"""

    x,y,z = center
    n = offset_radius
    v = array[x - n : x + n][y - n : y + n][z - n : z - n]
    if format_values == 0:
        return np.sum(v)
    elif format_values == 1:
        return np.average(v)
    else: 
        return v

global direction_dict_np, direction_keys

direction_dict_np = {
    'up' : np.asarray([0,0,1]),
    'left' : np.asarray([-1,0,0]),
    'down' : np.asarray([0,0,-1]),
    'right' : np.asarray([1,0,0]),
    'front' : np.asarray([0,-1,0]),
    'back' : np.asarray([0,1,0])
}
direction_keys = list(direction_dict_np.keys())
# print(direction_keys)[5]

def pheromon_loop(pheromon_layer, emmission_array = None, i = 1, blocking_layer = None, gravity_shift_bool = False, diffuse_bool = True, decay = True, decay_linear = False):
    """gravity direction: 0:left, 1:right, 2:front, 3:back, 4:down, 5:up"""
    for i in range(i):
        # emmission in
        if not isinstance(emmission_array, bool):
            pheromon_layer.emission_intake(emmission_array, 2, False)

        # diffuse
        if diffuse_bool:
            pheromon_layer.diffuse()

        # gravity
        if gravity_shift_bool:
            pheromon_layer.gravity_shift()

        # decay
        if decay_linear:
            pheromon_layer.decay_linear()
        elif decay:
            pheromon_layer.decay()

        # collision
        if blocking_layer != None:
            blocking_layer.block_layers([pheromon_layer])
        
        # apply gradient steps
        if pheromon_layer.gradient_resolution != 0:
            pheromon_layer.grade()

# def get_chance_by_climb_style(
#         agent, 
#         climb = 0.5,
#         top = 2,
#         walk = 0.1,
#         descend = -0.05,
#         chance_weight = 1):
#     "chance is updated based on the direction values and chance_weight"

#     last_moves = agent.move_history[-3:]
#     if last_moves == ['up', 'up', 'up']:
#         # climb_style = 'climb'
#         build_chance = climb
#     elif last_moves == ['up', 'up', 'side']:
#         # climb_style = 'top'
#         build_chance = top
#     elif last_moves == ['side', 'side', 'side']:
#         # climb_style = 'walk' 
#         build_chance = walk
#     elif last_moves == ['down', 'down', 'down']:
#         # climb_style = 'descend' 
#         build_chance = descend

#     build_chance *= chance_weight

#     return build_chance

# def get_chance_by_relative_position(
#         agent,
#         layer,
#         build_below = -1,
#         build_aside = -1,
#         build_above = 1,
#         build_strength = 1):
#     b, s, t = agent.analyze_relative_position(layer)
#     build_chance = (build_below * b + build_aside * s + build_above * t) * build_strength
#     return build_chance

# def get_chances_by_density(
#         agent, 
#         pheromone_layer,
#         radius,        
#         build_if_over = 0,
#         build_if_below = 5,
#         erase_if_over = 27,
#         erase_if_below = 0,
#         build_strength = 1):
#     """
#     returns build_chance, erase_chance
#     if layer nb value sum is between 
#     """
#     v = agent.scan_neighborhood_values(pheromone_layer, radius, agent.pose, format_values=0)

    
#     if build_if_over < v < build_if_below:
#         build_chance = build_strength
#     else:
#         build_chance = 0
#     if erase_if_over < v < erase_if_below:
#         erase_chance = 0
#     else:
#         erase_chance = build_strength
    
#     return build_chance, erase_chance

