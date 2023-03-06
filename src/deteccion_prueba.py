import Construct_verification as cr
import numpy as np
import cv2
import matplotlib.pyplot as plt 
import tensorflow as tf

print("Realsense object validator driver")

cv = cr.Construct_verification()
depth_frame, color_frame=cv.show_files(20,"./src/DataLayer/recording2.bag")

color_data = np.asanyarray(color_frame.get_data())
depth_data = np.asanyarray(depth_frame.get_data())

