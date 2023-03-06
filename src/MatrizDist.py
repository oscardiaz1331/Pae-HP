import math
import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
import pyrealsense2 as rs  
import Construct_verification as cr
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import preprocessing 
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from scipy.ndimage import label
# Setup:
pipe = rs.pipeline()
cfg = rs.config()
rs.config.enable_device_from_file(cfg , "../recordings/recordings/recording5.bag")
cfg.enable_stream(rs.stream.depth, rs.format.z16, 30)
cfg.enable_stream(rs.stream.color, rs.format.bgr8, 30)
profile = pipe.start(cfg)

cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)
  
# Create colorizer object
colorizer = rs.colorizer()

    # Streaming loop

verif = cr.Construct_verification()

#Representamos
depth_frame,color_frame = verif.show_files(15, "../recordings/recordings/recording1.bag")



#Assignamos valores de distancia de cada pixel en una matriz
matrizDist=[[0 for i in range(depth_frame.get_height())] for j in range(depth_frame.get_width())]
matrizBN = np.zeros(((depth_frame.get_width(), depth_frame.get_height())))


for height in range (1, (depth_frame.get_height())):
        for width in range (1, (depth_frame.get_width())):
                matrizDist[width][height]=depth_frame.get_distance(width,height)
                
maximo = max(max(fila) for fila in matrizDist)

for height in range (1, (depth_frame.get_height())):
        for width in range (1, (depth_frame.get_width())):
#                matrizDist[width][height]=depth_frame.get_distance(width,height)
                matrizBN[width][height]=int(math.trunc(depth_frame.get_distance(width,height)*255/maximo))
   

media = 0
pix = 0
for x in range (int((depth_frame.get_width()/2)-12), int((depth_frame.get_width()/2)+12)):
        for y in range ((int(depth_frame.get_height()/2)-12), int((depth_frame.get_height()/2)+12)):
                media +=  matrizDist[x][y]
                pix+=1



media = media/pix

print(media)

#print(matrizDist)
print(maximo) 
print(matrizBN)
vector = np.array(matrizDist).reshape(-1, 1)
kmeans=KMeans(n_clusters=5,n_init="auto")
kmeans.fit(vector)

labels = kmeans.labels_.reshape(len(matrizDist), len(matrizDist[0]))
labels = np.transpose(labels)
#for height in range (1, (depth_frame.get_height())):
 #       for width in range (1, (depth_frame.get_width())):
                
  #              matrizDist[width][height]=depth_frame.get_distance(width,height)
  
plt.imshow(labels)
plt.colorbar()
plt.show()
print(labels)
#labels_matriz = np.reshape(labels, (matrizDist.shape[0], matrizDist.shape[1]))
regiones,num_reg=label(labels)

# Mostramos las etiquetas de los clusters
plt.imshow(regiones)
plt.colorbar()
plt.show()


print((kmeans.labels_))
imagen_BW = cv2.normalize(matrizBN, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

cv2.imshow('Imagen en byn',matrizBN)


