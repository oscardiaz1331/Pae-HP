import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import cv2

import verification as v
import pyrealsense2 as rs
import CenterAverage as ca



pcd = o3d.io.read_point_cloud(".\gg\gg.ply")

#pcd = pcd.voxel_down_sample(voxel_size=0.02)  #down sampling por si imagen muy compleja
#o3d.visualization.draw_geometries([pcd]) 

pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
#pcd.remove_radius_outlier(nb_points=16, radius=0.05) # esta eliminacion tarda mucho si la imagen tiene muchos puntos
o3d.visualization.draw_geometries([pcd])   

#Empezamos probando segmentacion por planos

plane_model, inliers = pcd.segment_plane(distance_threshold=0.01, ransac_n=3,num_iterations=1000)
inlier_cloud = pcd.select_by_index(inliers)
inlier_cloud.paint_uniform_color([1.0, 0, 0])
outlier_cloud = pcd.select_by_index(inliers, invert=True)     
o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])  
pcd = outlier_cloud

plane_model, inliers = pcd.segment_plane(distance_threshold=0.02, ransac_n=3,num_iterations=1000)
inlier_cloud = pcd.select_by_index(inliers)
outlier_cloud = pcd.select_by_index(inliers, invert=True) 
inlier_cloud.paint_uniform_color([1.0, 0, 0])
outlier_cloud.paint_uniform_color([1.0, 0, 0])
o3d.visualization.draw_geometries([inlier_cloud]) 
o3d.visualization.draw_geometries([outlier_cloud]) 
pcd = outlier_cloud



#Ahora segmentacion con DBSCAN

with o3d.utility.VerbosityContextManager(
        o3d.utility.VerbosityLevel.Debug) as cm:
    labels = np.array(
        pcd.cluster_dbscan(eps=0.00309, min_points=50, print_progress=True)) # con imagenes donde objeto tiene depth parecido eps=0.0018 , y cuando no  eps=0.003

max_label = labels.max()
print(f"point cloud has {max_label + 1} clusters")
colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
colors[labels < 0] = 0
pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
o3d.visualization.draw_geometries([pcd])


 
#Buscamos la region que nos interesa
target_label= 0
selected_indices = np.where(labels == target_label)[0]
selected_pcd = pcd.select_by_index(selected_indices)
max_pcd= selected_pcd


for i in range(max_label):
    target_label = i
    if(target_label> 0):
        selected_indices = np.where(labels == target_label)[0]
        selected_pcd = pcd.select_by_index(selected_indices)

        if( np.asarray(selected_pcd.points).size> np.asarray(max_pcd.points).size):
            max2_pcd = max_pcd
            max_pcd= selected_pcd
            break
        if(i==1):
            max2_pcd= selected_pcd

        if( np.asarray(selected_pcd.points).size > np.asarray(max2_pcd.points).size ):
            max2_pcd = selected_pcd
            
o3d.visualization.draw_geometries([max_pcd])
o3d.visualization.draw_geometries([max2_pcd])
max_points = np.asarray(max_pcd.points)
max_points2 = np.asarray(max2_pcd.points)


if( np.var(max_points[:,2]) > np.var(max_points2[:,2])):
    pcd_final = max_pcd
else:
    pcd_final = max2_pcd

o3d.visualization.draw_geometries([pcd_final])

#esta transformacion teniendo en cuenta pos y angulo de la camara la podriamos hacer al principio, tambien hay que mirar si av distance se puede hacer directamente o hay q hacerlo sobre pcd inicial
# Define camera position and orientation in real world coordinates
camera_pos = np.array([0, 0, 0])
camera_rot = np.eye(3)  # Identity rotation matrix

# Transform point cloud to camera coordinate system
pcd_final.translate(-camera_pos)
pcd_final.rotate(camera_rot, center=(0, 0, 0))

# Calculate distances of points to camera position
distances = np.linalg.norm(np.asarray(pcd_final.points), axis=1)

# Calculate average distance
avg_distance = np.mean(distances)

print("Average distance from camera to points:", avg_distance)

'''
# Define camera extrinsic parameters (translation and rotation)
camera_pos = np.array([0, 0, 1]) # example camera position
camera_rot = np.eye(3) # example camera rotation

# Define camera intrinsic parameters (focal length and principal point)
focal_length = 1000 # example focal length
principal_point = (640, 480) # example principal point

# Create transformation matrix from camera parameters
intrinsic = o3d.camera.PinholeCameraIntrinsic(640, 480, focal_length, focal_length, *principal_point)
extrinsic = np.eye(4)
extrinsic[:3,:3] = camera_rot
extrinsic[:3,3] = camera_pos
transformation_matrix = intrinsic.intrinsic_matrix @ extrinsic

# Transform camera position to point cloud coordinate system
camera_pos_pcd = np.linalg.inv(transformation_matrix) @ np.append(camera_pos, 1)
print("Camera position in point cloud coordinate system:", camera_pos_pcd[:3])
camera_pos= camera_pos_pcd[:3]

#camera_pos = np.array([0, 0, 1]) # example camera position

# Compute distances between camera position and points in point cloud
distances = np.linalg.norm(np.asarray(pcd.points) - camera_pos, axis=1)

# Calculate average distance
avg_distance = np.mean(distances)
'''


'''
# Una vez tenemos segmentado el obejto de interes calculamos la media de distancia

#Convert the points numpy array to a 2D numpy array
points_array = np.asarray(pcd_final.points)

# Define the origin of the space
origin = np.array([0.0, 0.0, 0.0])

# Calculate the distances between the origin and each point
distances = np.linalg.norm(points_array - origin, axis=1)

# Compute the average of the distances
avg_distance = np.mean(distances)
# Compute the variance of the distances
variance = np.var(distances)
print("The average distance between the origin and the points in the point cloud is: ", avg_distance)
print("The variance distance between the origin and the points in the point cloud is: ", variance)
'''