import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
import pyrealsense2 as rs  

# Setup:
pipe = rs.pipeline()
cfg = rs.config()
rs.config.enable_device_from_file(cfg , "./recroding.bag")
cfg.enable_stream(rs.stream.depth, rs.format.z16, 30)
profile = pipe.start(cfg)

cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)
  
# Create colorizer object
colorizer = rs.colorizer()

    # Streaming loop
while True:
        # Get frameset of depth
        frames = pipe.wait_for_frames()

        # Get depth frame
        depth_frame = frames.get_depth_frame()

        # Colorize depth frame to jet colormap
        depth_color_frame = colorizer.colorize(depth_frame)

        # Convert depth_frame to numpy array to render image in opencv
        depth_color_image = np.asanyarray(depth_color_frame.get_data())

        # Render image in opencv window
        cv2.imshow("Depth Stream", depth_color_image)
        key = cv2.waitKey(1)
        # if pressed escape exit program
        if key == 27:
            cv2.destroyAllWindows()
            break