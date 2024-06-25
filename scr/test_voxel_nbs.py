import numpy as np
import show_voxel_plt as show

a = np.zeros(8)
a = a.reshape(2,2,2)
a[0,0,0] = 0.51
a[1,0,0] = 0.02
up = np.roll(a, 1, 0)
down = np.roll(a, -1, 0)
front = np.roll(a, -1, 1)
back = np.roll(a, 1, 1)
left = np.roll(a, -1, 2)
right = np.roll(a, 1, 2)

nb_mask = {
    'u' : [1, 0],
    'd' : [-1, 0],
    'f' : [-1, 1],
    'b' : [1, -1],
    'l' : [-1, 2],
    'r' : [1, 2]}


print('initial\n', a, '\n0. Z. up\n', up, '\n1., Y, front\n', front, '\n2. X, left\n', left)

show.show_voxel(a)