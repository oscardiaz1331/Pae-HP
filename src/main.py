from CalculeK import CalculateK
from Kmeans import Kmeans
from MatrizDist import MatrizDist
from SetupCamera import SetupCamera


depth_frame, color_frame = SetupCamera("../recordings/recordings/recording4.bag")
matrizDist = MatrizDist(depth_frame)
numLabels = Kmeans(matrizDist)
#print(CalculateK(matrizDist))