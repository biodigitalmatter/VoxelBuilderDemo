from voxel_builder_library import *
import numpy as np

v = Layer('Test', 2)
v.random()
larger = np.nonzero(v.array > 0.5)
print(v.array)
print(v.array[:,:,:][v.array > 0.5])
print(np.asarray(larger).transpose())

