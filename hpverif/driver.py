import verification as v
from pyntcloud import PyntCloud
import open3d as o3d
import numpy as np
import open3d as o3d
from sklearn.cluster import KMeans, DBSCAN, OPTICS
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

pcd = o3d.io.read_point_cloud("./4.ply")
# Get points and transform it to a numpy array:
points = np.asarray(pcd.points).copy()

scaled_points = StandardScaler().fit_transform(points)
# Clustering:
model = KMeans(n_clusters=4)
model.fit(scaled_points)
print("s")


labels = model.labels_
# Get the number of colors:
n_clusters = len(set(labels))

# Mapping the labels classes to a color map:
colors = plt.get_cmap("tab20")(labels / (n_clusters if n_clusters > 0 else 1))
# Attribute to noise the black color:
colors[labels < 0] = 0
# Update points colors:
pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])

# Display:
o3d.visualization.draw_geometries([pcd])