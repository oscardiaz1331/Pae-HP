from Calibraton import Calibration
from frameCapture import Frame_Capture
from showFiles import Show_Files
from matrixDist import MatrixDiagnose
from Kmeans import Kmeans


class Verification:
    def __init__ (self):
        pass

    
    def calibration(self):
        calibrate = Calibration()
        calibrate.enable_stream()
        calibrate.calibrate()


    def capture_frame(self,frames, filename, high):
        frame_capture = Frame_Capture()
        frame_capture.get_and_configure_device()
        return frame_capture.capture(frames, filename, high)

    def show_files(self, frame,  filename):
        show = Show_Files()
        show.enable_file(filename)
        return show.show(frame)
    
    def matrixDiagn (self, depthFrame):
        matrixD = MatrixDiagnose(depthFrame)
        finalMatrix = matrixD.MatrizDist(depthFrame)
        return finalMatrix
    
    def kmeans (self,matrix, k):
        km = Kmeans()
        km.CalculateKMeans(matrix, k)
        