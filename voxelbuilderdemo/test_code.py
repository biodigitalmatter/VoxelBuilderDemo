import numpy as np

a = np.random.randint(10, size=[8,3])
print(a)
b = np.clip(0,2,a)
print(b)