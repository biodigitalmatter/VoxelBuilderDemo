import numpy as np
from class_agent import Agent


agent = Agent()
print(agent.pose)
agent.pose = [2,2,2]
print(agent.pose)
x_radius = 1
y_radius = 1
z_radius = 1
x_offset = -2
y_offset = -2
z_offset = -2

n=3
array = np.random.randint(10, size=[n,n,n])

v = agent.get_nb_slice_parametric(array,
    x_radius,
    y_radius,
    z_radius,
    x_offset,
    y_offset,
    z_offset,
    format_values=2
)

print(v)
