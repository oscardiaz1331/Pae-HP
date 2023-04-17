from Calibraton import Calibration
from frameCapture import Frame_Capture
from showFiles import Show_Files
from frameCapturePLY import Frame_Capture_PLY
from pointCloud import PointCloud
from segmentation import Segmentation
import numpy as np

class Verification:
    def __init__ (self):
        pass

    
    def calibration(self):
        calibrate = Calibration()
        calibrate.enable_stream()
        calibrate.calibrate()


    def capture_frame(self,frames, filename, high):
        frame_capture = Frame_Capture()
        frame_capture.get_and_configure_device(high)
        return frame_capture.capture(frames, filename, high)
    
    def capture_frame_ply(self,filename, high):
        frame_capture = Frame_Capture_PLY()
        frame_capture.get_and_configure_device()
        frame_capture.capture(filename, high)

    def show_files(self, frame,  filename):
        show = Show_Files()
        show.enable_file(filename)
        return show.show(frame)
    
    #def kmeans (self,matrix, k):
      #  km = Kmeans()
       # km.CalculateKMeans(matrix, k)
    
    def PointCloud (self, dp, filename):
        pc = PointCloud()
        return pc.createPointCloud(0.001*np.asanyarray(dp.get_data()),filename)
        
    
    def Segmentation (self, filename ):
        seg = Segmentation(filename)
        seg.removeBackgorund()
        return seg.segmentation()
        