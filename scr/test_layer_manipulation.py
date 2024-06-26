from voxel_builder_library import *
from show_voxel_plt import *
import numpy as np

# Test conditional formatting
v = Layer('Test', 5)
v.random()
v.conditional_fill('<', 0.1,  override_self=True)
show_voxel(v.array)

