import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
config = rs.config()
config.enable_device('017322075378')
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)
config.enable_stream(rs.stream.accel)
config.enable_stream(rs.stream.gyro)


       


pipe_profile = pipeline.start(config)

depth_sensor = pipe_profile.get_device().first_depth_sensor()

#Activem High Accuracy Mode (3); High Density (4)
visualpreset = depth_sensor.get_option_value_description(rs.option.visual_preset,4)
depth_sensor.set_option(rs.option.visual_preset, 4)


try:
    for i in range(1000):

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        if(i==10):
            fin_depth_image = depth_image
            fin_color_image = color_image

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
        cv2.waitKey(1)

finally:

    # Stop streaming
    pipeline.stop()



#print('preset range:'+str(preset_range))
#for i in range(int(preset_range.max)):
    
 #   print('%02d: %s'%(i,visulpreset))
 #   if visulpreset == "High Accuracy":
  #      depth_sensor.set_option(rs.option.visual_preset, i)

