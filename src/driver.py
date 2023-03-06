import Construct_verification as cr
filesource = "./src/DataLayer/"


print("Realsense object validator driver")

verif = cr.Construct_verification()

dp,cl = verif.show_files(20, filesource + "gege.bag")
print(dp,cl)