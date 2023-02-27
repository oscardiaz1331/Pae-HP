import Construct_verification as cr

print("Realsense object validator driver")

verif = cr.Construct_verification()

verif.capture_frame(100,'prueba.bag')