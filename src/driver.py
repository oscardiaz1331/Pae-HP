import Construct_verification as cr
filesource = "./src/DataLayer/"


print("Realsense object validator driver")

verif = cr.Construct_verification()

dp,cl = verif.show_files(20, filesource + "/recordings/recording1.bag")
print(dp,cl)