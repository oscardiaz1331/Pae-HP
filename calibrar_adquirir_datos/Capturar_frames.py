import pyrealsense2 as rs
import numpy as np
import cv2
import matplotlib.pyplot as plt   

pipe = rs.pipeline()
cfg = rs.config()
cfg.enable_stream(rs.stream.depth)
pipe.start(cfg)

try:
    for x in range(50):
        # Wait for the next set of frames from the camera
        frames = pipe.wait_for_frames()

        # Fetch pose frame
        depth = frames.get_depth_frame()
        
        
        
            

finally:
    pipe.stop()

colorizer = rs.colorizer()
colorized_depth = np.asanyarray(colorizer.colorize(depth))
plt.imshow(colorized_depth)    