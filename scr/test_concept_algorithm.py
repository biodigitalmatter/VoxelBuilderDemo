import numpy as np

# create empty
n = 30
voxel = np.zeros([n,n,n])
# add ground
voxel[:,:,0] = 1

agent_positions = []
for i in range(3):
    dir = np.random.randint(-1, [2,2,2])
    print(dir)