    
import pyrealsense2 as rs
import numpy as np
import cv2


class Calibration:
   
    def __init__ (self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()

    def enable_stream(self):
    
        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = self.config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        found_rgb = False
        for s in device.sensors:
            if s.get_info(rs.camera_info.name) == 'RGB Camera':
                found_rgb = True
                break
        if not found_rgb:
            print("The demo requires Depth camera with Color sensor")
            exit(0)

        self.config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

        if device_product_line == 'L500':
            self.config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
        else:
            self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        
        


    def calibrate (self):
    # Start streaming
        self.pipeline.start(self.config)
        depth_frame_set={}
        color_frame_set={}
        for x in range(20):
                # Wait for a coherent pair of frames: depth and color
                frames = self.pipeline.wait_for_frames()
                depth_frame_set[x] = frames.get_depth_frame()
                color_frame_set[x] = frames.get_color_frame()
                if not depth_frame_set[x] or not color_frame_set[x]:
                    continue

                # Convert images to numpy arrays
                depth_image = np.asanyarray(depth_frame_set[x].get_data())
                color_image = np.asanyarray(color_frame_set[x].get_data())

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



            # Stop streaming
        self.pipeline.stop()


        f = open ("./output.txt", "w")
        f.write( depth_frame_set[1])
        f.close()

