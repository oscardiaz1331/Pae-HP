import math
import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
import pyrealsense2 as rs  

# Setup:
pipe = rs.pipeline()
cfg = rs.config()
rs.config.enable_device_from_file(cfg , "../recordings/recordings/recording1.bag")
cfg.enable_stream(rs.stream.depth, rs.format.z16, 30)
cfg.enable_stream(rs.stream.color, rs.format.bgr8, 30)
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
depth_frame1 = frames.get_depth_frame()
color_frame = frames.get_color_frame()


#Assignamos valores de distancia de cada pixel en una matriz
matrizDist=[[0 for i in range(depth_frame.get_height())] for j in range(depth_frame.get_width())]
matrizBN=[[0 for i in range(depth_frame.get_height())] for j in range(depth_frame.get_width())]

for height in range (1, (depth_frame.get_height())):
        for width in range (1, (depth_frame.get_width())):
                matrizDist[width][height]=depth_frame.get_distance(width,height)
                
maximo = max(max(fila) for fila in matrizDist)

for height in range (1, (depth_frame.get_height())):
        for width in range (1, (depth_frame.get_width())):
                matrizDist[width][height]=depth_frame.get_distance(width,height)
                matrizBN[width][height]=int(math.trunc(depth_frame.get_distance(width,height)*256/maximo-1))
   

print(matrizDist)
print(maximo) 

#for x in range(30):
        # Wait for a coherent pair of frames: depth and color
        #frames = pipe.wait_for_frames()


if not depth_frame:
       print("no depth")

if not color_frame:
       print("no color")


# Convert images to numpy arrays
depth_image = np.asanyarray(depth_frame.get_data())
color_image = np.asanyarray(color_frame.get_data())

# Apply colormap on depth image (image must be converted to 8-bit per pixel first)
depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

depth_colormap_dim = depth_colormap.shape
color_colormap_dim = color_image.shape

# If depth and color resolutions are different, resize color image to match depth image for display
if depth_colormap_dim != color_colormap_dim:
    resized_color_image = cv2.resize(color_image, dsize=(depth_colormap_dim[1], depth_colormap_dim[0]), interpolation=cv2.INTER_AREA)
    images = np.hstack((resized_color_image, depth_colormap))
else:
    images = np.hstack((color_image, depth_colormap))

# Show images
cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
cv2.imshow('RealSense', images)

print(depth_frame)

print(color_frame)