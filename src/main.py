from CalculeK import CalculateK
from Kmeans import Kmeans
from MatrizDist import MatrizDist
from SetupCamera import SetupCamera


depth_frame, color_frame = SetupCamera("../recordings/recordings/recording1.bag")
matrizDist = MatrizDist(depth_frame)

k=CalculateK(matrizDist)
if(k>=6):
    numLabels = Kmeans(matrizDist,2)
else:
    numLabels = Kmeans(matrizDist,k)
