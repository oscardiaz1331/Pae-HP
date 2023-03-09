import math
import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
import pyrealsense2 as rs  
import Construct_verification as cr
from scipy.ndimage import label

def MatrizDist(depth_frame):
        #Assignamos valores de distancia de cada pixel en una matriz
        matrizDist=[[0 for i in range(depth_frame.get_height())] for j in range(depth_frame.get_width())]
        for height in range (1, (depth_frame.get_height())):
                for width in range (1, (depth_frame.get_width())):
                        matrizDist[width][height]=depth_frame.get_distance(width,height)
        return matrizDist
        #matrizBN = np.zeros(((depth_frame.get_width(), depth_frame.get_height())))
        # maximo = max(max(fila) for fila in matrizDist)
        #for height in range (1, (depth_frame.get_height())):
         #       for width in range (1, (depth_frame.get_width())):
          #              matrizBN[width][height]=int(math.trunc(depth_frame.get_distance(width,height)*255/maximo))
        




       # imagen_BW = cv2.normalize(matrizBN, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)

       # cv2.imshow('Imagen en byn',matrizBN)
        
        #separar la funcion de representacion, la funcion que hace la matriz de distancias y el kmeans
