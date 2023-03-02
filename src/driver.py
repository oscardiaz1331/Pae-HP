import Construct_verification as cr
filesource = "./src/DataLayer/"


print("Realsense object validator driver")

verif = cr.Construct_verification()

dp, cl = verif.capture_frame(100, "gege.bag")
print(dp)