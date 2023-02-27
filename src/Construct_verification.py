from DomainLayer.Classes.Calibraton import Calibration
from DomainLayer.Classes.Frame_Capture import Frame_Capture
from DomainLayer.Classes.Show_Files import Show_Files



class Construct_verification:
    def __init__ (self):
        pass

    
    def calibration():
        calibrate = Calibration()
        calibrate.enable_stream()
        calibrate.calibrate()


    def capture_frame(frames, filename):
        frame_capture = Frame_Capture()
        frame_capture.get_and_configure_device()
        frame_capture.capture(frames, filename)

    def show_files(filename):
        show = Show_Files()
        show.enable_file(filename)
        show.show()

        





