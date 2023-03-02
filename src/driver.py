import Construct_verification as cr
filesource = "./src/DataLayer/"


print("Realsense object validator driver")

verif = cr.Construct_verification()

verif.show_files(filesource+ "prueba.bag")