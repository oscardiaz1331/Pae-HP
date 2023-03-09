import numpy as np                       
import matplotlib.pyplot as plt          
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from scipy.ndimage import label

def Kmeans(matrizDist,k):    
    vector = np.array(matrizDist).reshape(-1, 1)
    kmeans=KMeans(n_clusters=k+1,n_init="auto")
    kmeans.fit(vector)

    labels = kmeans.labels_.reshape(len(matrizDist), len(matrizDist[0]))
    labels = np.transpose(labels)
    #for height in range (1, (depth_frame.get_height())):
    #       for width in range (1, (depth_frame.get_width())):
                    
    #              matrizDist[width][height]=depth_frame.get_distance(width,height)
    
    plt.imshow(labels)
    plt.colorbar()
    plt.show()

    #labels_matriz = np.reshape(labels, (matrizDist.shape[0], matrizDist.shape[1]))
    regiones,num_reg=label(labels)

    # Mostramos las etiquetas de los clusters
    plt.imshow(regiones)
    plt.colorbar()
    plt.show()
    return labels
