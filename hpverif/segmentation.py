import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt



class Segmentation:

    def __init__(self,filename,min,max) :
        self.pcd =   o3d.io.read_point_cloud(filename)
        #pcd =self.pcd.voxel_down_sample(voxel_size=0.02)  #down sampling por si imagen muy compleja
        self.pcd.remove_statistical_outlier(nb_neighbors= 10, std_ratio=2.0)
        o3d.visualization.draw_geometries([self.pcd]) 
        self.min = min
        self.max = max
        #pcd.remove_radius_outlier(nb_points=16, radius=0.05) # esta eliminacion tarda mucho si la imagen tiene muchos puntos


    def removeBackgorund(self):
    
        plane_model, inliers =self.pcd.segment_plane(distance_threshold=3.5, ransac_n=3,num_iterations=1000) #0.01. El q funcionaba bien era 0.008
        inlier_cloud = self.pcd.select_by_index(inliers)
        inlier_cloud.paint_uniform_color([1.0, 0, 0])
        outlier_cloud =self.pcd.select_by_index(inliers, invert=True)     
        #o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])  
        self.pcd = outlier_cloud
 
        depth_values_plane= np.asarray(inlier_cloud.points)[:,2] 
        depth_value_plane= ((np.mean(depth_values_plane)/255)*self.max)+self.min
        print("distancia pared final: " + str(depth_value_plane))


        # Podriamos mirar a partir de la inclinacion del plano cde la pared(que se detecta bien en todos los casos)para saber que aproach utilizar. Si estamos en caso de todo recto- dos segmentaciones de planos. Si caso inclinado 1 plano 1 dbscan

        plane_model, inliers =self.pcd.segment_plane(distance_threshold=2.8, ransac_n=3,num_iterations=1000) #2.8
        inlier_cloud =self.pcd.select_by_index(inliers)
        outlier_cloud =self.pcd.select_by_index(inliers, invert=True) 
        inlier_cloud.paint_uniform_color([1.0, 0, 0])
        outlier_cloud.paint_uniform_color([1.0, 0, 0])
        o3d.visualization.draw_geometries([inlier_cloud]) 
        o3d.visualization.draw_geometries([outlier_cloud]) 
        self.pcd = outlier_cloud

        depth_values_plane= np.asarray(inlier_cloud.points)[:,2] 
        depth_value_plane= ((np.mean(depth_values_plane)/255)*self.max)+self.min
        print("distancia suelo/objeto: " + str(depth_value_plane))

        



    def segmentation(self):   

        with o3d.utility.VerbosityContextManager(
        o3d.utility.VerbosityLevel.Debug) as cm:
            labels = np.array(
               self.pcd.cluster_dbscan(eps=3.2, min_points=20, print_progress=True)) # inclinado: 3.2, y min_p=50.     1.8

        max_label = labels.max()
        print(f"point cloud has {max_label + 1} clusters")
        colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
        colors[labels < 0] = 0
        self.pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
        o3d.visualization.draw_geometries([self.pcd])


        
        #Buscamos la region que nos interesa
        target_label= 0
        selected_indices = np.where(labels == target_label)[0]
        selected_pcd =self.pcd.select_by_index(selected_indices)
        max_pcd= selected_pcd


        for i in range(max_label):
            target_label = i
            if(target_label> 0):
                selected_indices = np.where(labels == target_label)[0]
                selected_pcd =self.pcd.select_by_index(selected_indices)

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

        if(np.var(max_points2[:,2])<np.var(max_points2[:,2])):
            pcd_final=max2_pcd
        else:
            pcd_final=max_pcd


        o3d.visualization.draw_geometries([pcd_final])

        depth_values_obj= np.asarray(pcd_final.points)[:,2] 
        depth_value_plane= ((np.mean(depth_values_obj)/255)*self.max)+self.min
        print(depth_value_plane)