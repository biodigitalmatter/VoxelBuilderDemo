from compas.geometry import Pointcloud

file = 'test_compas_point_cloud.json'
ptcloud = Pointcloud.from_json(file)
print(ptcloud)