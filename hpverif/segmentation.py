import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt



class Segmentation:

    def __init__(self,filename) :
        self.pcd =   o3d.io.read_point_cloud(filename)
        #pcd = pcd.voxel_down_sample(voxel_size=0.02)  #down sampling por si imagen muy compleja
        #o3d.visualization.draw_geometries([pcd]) 
        self.pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.0)
        #pcd.remove_radius_outlier(nb_points=16, radius=0.05) # esta eliminacion tarda mucho si la imagen tiene muchos puntos


    def removeBackgorund(self):
    
        #Empezamos probando segmentacion por planos
        plane_model, inliers = self.pcd.segment_plane(distance_threshold=0.01, ransac_n=3,num_iterations=1000)
        inlier_cloud = self.pcd.select_by_index(inliers)
        inlier_cloud.paint_uniform_color([1.0, 0, 0])
        outlier_cloud = self.pcd.select_by_index(inliers, invert=True)     
        o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])  
        self.pcd = outlier_cloud

        #Ahora segmentacion con DBSCAN

        



    def segmentation(self):   

        with o3d.utility.VerbosityContextManager(
                o3d.utility.VerbosityLevel.Debug) as cm:
            labels = np.array(
                self.pcd.cluster_dbscan(eps=0.0018, min_points=50, print_progress=True)) # con imagenes donde objeto tiene depth parecido eps=0.0018 , y cuando no  eps=0.003

        max_label = self.labels.max()
        print(f"point cloud has {max_label + 1} clusters")
        colors = plt.get_cmap("tab20")(self.labels / (max_label if max_label > 0 else 1))
        colors[self.labels < 0] = 0
        self.pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
        o3d.visualization.draw_geometries([self.pcd])
     
        #Buscamos la region que nos interesa
        target_label= 0
        selected_indices = np.where(self.labels == target_label)[0]
        selected_pcd = self.pcd.select_by_index(selected_indices)
        max_pcd= selected_pcd
        max2_pcd = selected_pcd
        for i in range(max_label):
            target_label = i
            if(target_label> 0):
                selected_indices = np.where(labels == target_label)[0]
                selected_pcd = self.pcd.select_by_index(selected_indices)
                if( np.asarray(selected_pcd.points).size> np.asarray(max_pcd.points).size):
                    max_pcd= selected_pcd
                    break
                if( np.asarray(selected_pcd.points).size > np.asarray(max2_pcd.points).size):
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
        return labels, self.pcd