    
import pyrealsense2 as rs
import numpy as np
import cv2


class Frame_Capture:
   
    def __init__ (self):
        self.pipeline = rs.pipeline()
        self.config = rs.config()

    