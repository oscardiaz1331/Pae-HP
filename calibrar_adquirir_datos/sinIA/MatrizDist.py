import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
import pyrealsense2 as rs  

# Setup:
pipe = rs.pipeline()
cfg = rs.config()
rs.config.enable_device_from_file(cfg , "../recordings/recordings/recording1.bag")
cfg.enable_stream(rs.stream.depth, rs.format.z16, 30)
profile = pipe.start(cfg)

cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)
  
# Create colorizer object
colorizer = rs.colorizer()

    # Streaming loop
#while True:
        # Get frameset of depth
frames = pipe.wait_for_frames()

# Get depth frame
depth_frame = frames.get_depth_frame()

x = 320
y = 240

#Assignamos valores de distancia de cada pixel en una matriz
matrizDist=[[0 for i in range(depth_frame.get_height())] for j in range(depth_frame.get_width())]

for height in range (1, (depth_frame.get_height())):
        for width in range (1, (depth_frame.get_width())):
                matrizDist[width][height]=depth_frame.get_distance(width,height)
                
maximo = max(max(fila) for fila in matrizDist)
  

#Normalizamos y procesamos
for height in range (1, (depth_frame.get_height())):
        for width in range (1, (depth_frame.get_width())):
                matrizDist[width][height]=matrizDist[width][height]*100/maximo


print(depth_frame.get_height())
print(matrizDist)
print(maximo)    