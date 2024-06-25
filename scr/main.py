# test functions

import voxel_builder_library as builder
import show_voxel_plt as view
import numpy as np

n = 120

smells = builder.Layer('air', voxel_size = n)
smells.rgb = [0,1,0.2]
smells.random(add = -0.5, crop=True, strech=2)
# view.show_voxel(smells.array, smells.colors)
# for i in range(5):
smells.diffuse(repeat=1)
# view.show_voxel(smells.array, smells.colors)
print(smells.__repr__)