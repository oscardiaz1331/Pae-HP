import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
import cv2
import math
import verification as v
import pyrealsense2 as rs
import CenterAverage as ca


import verification  as v



verif = v.Verification()
dp,dc,p = verif.show_files(26,"prueba50cm.bag")

min, max, fact = verif.PointCloud(dp,"prueba50cm")

pcd = o3d.io.read_point_cloud("prueba50cm/prueba50cm.ply")
#pcd = pcd.voxel_down_sample(voxel_size=0.02)  #down sampling por si imagen muy compleja
#o3d.visualization.draw_geometries([pcd]) 

pcd.remove_statistical_outlier(nb_neighbors=10, std_ratio=2.0)
#pcd.remove_radius_outlier(nb_points=16, radius=0.05) # esta eliminacion tarda mucho si la imagen tiene muchos puntos
o3d.visualization.draw_geometries([pcd])   

#Empezamos probando segmentacion por planos
restr= 0
if(max-min> 1):
    rest = 0.035
else:
    rest = 0.02

plane_model, inliers = pcd.segment_plane(distance_threshold=(((rest - min) / max)*fact), ransac_n=3,num_iterations=1000) #0.02. El q funcionaba bien era 0.008 #3
[a, b, c, d] = plane_model
print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
theta = (math.acos(abs(c) / math.sqrt(a**2 + b**2 + c**2)))*180/math.pi
print(f"theta:{theta:.2f}")
inlier_cloud = pcd.select_by_index(inliers)
inlier_cloud.paint_uniform_color([1.0, 0, 0])
outlier_cloud = pcd.select_by_index(inliers, invert=True)     
o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])  
pcd = outlier_cloud

depth_values_plane= np.asarray(inlier_cloud.points)[:,2] 
depth_value_plane= ((np.mean(depth_values_plane)/fact)*max)+min
print("distancia pared final: " + str(depth_value_plane))


plane_model, inliers = pcd.segment_plane(distance_threshold=(((0.015 - min) / max)*fact), ransac_n=3,num_iterations=1000) #2.8
[a, b, c, d] = plane_model
print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
inlier_cloud = pcd.select_by_index(inliers)
outlier_cloud = pcd.select_by_index(inliers, invert=True) 
inlier_cloud.paint_uniform_color([1.0, 0, 0])
outlier_cloud.paint_uniform_color([1.0, 0, 0])
o3d.visualization.draw_geometries([inlier_cloud]) 
o3d.visualization.draw_geometries([outlier_cloud]) 
pcd = outlier_cloud

depth_values_plane= np.asarray(inlier_cloud.points)[:,2] 
depth_value_plane= ((np.mean(depth_values_plane)/fact)*max)+min
if(theta < 8):
    print("distancia segundo objeto plano/suelo: " + str(depth_value_plane))
else:
    print("distancia suelo: " + str(depth_value_plane))
  



'''
# Podriamos mirar a partir de la inclinacion del plano cde la pared(que se detecta bien en todos los casos)para saber que aproach utilizar. Si estamos en caso de todo recto- dos segmentaciones de planos. Si caso inclinado 1 plano 1 dbscan
#podriamos tambien ir girando el pointcloud para ir eliminando las paredes laterales
plane_model, inliers = pcd.segment_plane(distance_threshold=(((0.02 - min) / max)*fact), ransac_n=3,num_iterations=1000) #2.8
[a, b, c, d] = plane_model
print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
inlier_cloud = pcd.select_by_index(inliers)
outlier_cloud = pcd.select_by_index(inliers, invert=True) 
inlier_cloud.paint_uniform_color([1.0, 0, 0])
outlier_cloud.paint_uniform_color([1.0, 0, 0])
o3d.visualization.draw_geometries([inlier_cloud]) 
o3d.visualization.draw_geometries([outlier_cloud]) 
pcd = outlier_cloud

depth_values_plane= np.asarray(inlier_cloud.points)[:,2] 
depth_value_plane= ((np.mean(depth_values_plane)/1024)*max)+min
print("distancia suelo/objeto: " + str(depth_value_plane))
'''

if(theta>8): 
#Ahora segmentacion con DBSCAN

    with o3d.utility.VerbosityContextManager(
            o3d.utility.VerbosityLevel.Debug) as cm:
        labels = np.array(
            pcd.cluster_dbscan(eps=(((0.03 - min) / max)*fact), min_points=50, print_progress=True)) # inclinado: 3.2, y min_p=50.     1.8

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

            if(i==1):
                max2_pcd= selected_pcd
        
            if( len(selected_pcd.points) > len(max2_pcd.points) ):
                max2_pcd = selected_pcd

            if( len(selected_pcd.points)> len(max_pcd.points)):  # np.asarray(selected_pcd.points).size> np.asarray(max_pcd.points).size
                max2_pcd = max_pcd
                max_pcd= selected_pcd
            
    o3d.visualization.draw_geometries([max_pcd])
    o3d.visualization.draw_geometries([max2_pcd])
    max_points = np.asarray(max_pcd.points)
    max_points2 = np.asarray(max2_pcd.points)

    print("varianza:" + str(np.var(max_points2[:,2])))

    print("varianza:" + str(np.var(max_points[:,2])))

    ''' 
    if( (np.var(max_points[:,2]) <= np.var(max_points[:,2]) +1.2*np.var(max_points2[:,2]))):
        pcd_final = max_pcd
    elif(np.var(max_points2[:,2])<0.8*np.var(max_points[:,2]) ):
        pcd_final = max2_pcd
    else:
        pcd_final= max_pcd
    '''
    if(np.var(max_points2[:,2])<np.var(max_points2[:,2])):
        pcd_final=max2_pcd
    else:
        pcd_final=max_pcd


    o3d.visualization.draw_geometries([pcd_final])

    depth_values_obj= np.asarray(pcd_final.points)[:,2] 
    depth_value_plane= ((np.mean(depth_values_obj)/fact)*max)+min
    print("distancia objeto inclinado: " + str(depth_value_plane))



#(media/255)*max+min

'''
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