import cv2                              
import pyrealsense2 as rs  
import Construct_verification as cr

def SetupCamera(imagen):
    # Setup:
    pipe = rs.pipeline()
    cfg = rs.config()
    rs.config.enable_device_from_file(cfg , imagen) #"../recordings/recordings/recording5.bag"
    cfg.enable_stream(rs.stream.depth, rs.format.z16, 30)
    cfg.enable_stream(rs.stream.color, rs.format.bgr8, 30)
    profile = pipe.start(cfg)
    cv2.namedWindow("Depth Stream", cv2.WINDOW_AUTOSIZE)
    # Create colorizer object
    colorizer = rs.colorizer()
        # Streaming loop
    verif = cr.Construct_verification()
    #Representamos
    depth_frame,color_frame = verif.show_files(15, imagen)
    return depth_frame, color_frame

