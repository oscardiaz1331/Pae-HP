import verification as v
import pyrealsense2 as rs
import CenterAverage as ca


verif = v.Verification()
dp,cp = verif.capture_frame(130,"MedAcc.bag",4)

#s = verif.matrixDiagn(dp)




