import math
import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
import pyrealsense2 as rs  
from scipy.ndimage import label
from collections import deque as queue


class MatrixDiagnose:
    
 
        def __init__ (self, depth_frame):
        # Direction vectors
            self.dRow = [ -1, 0, 1, 0]
            self.dCol = [ 0, 1, 0, -1]
            self.height = depth_frame.get_height()
            self.width = depth_frame.get_width()
            self.vis = vis = [[ False for i in range(self.height)] for j in range(self.width)]
            self.total = 0
    
        def MatrizDist(self,depth_frame):
            to_change = []
            new_values = []
            #Assignamos valores de distancia de cada pixel en una matriz
            matrizDist=[[0 for i in range(self.height)] for j in range(self.width)]
            for height in range (0, (self.height)):
                    for width in range (0, (self.width)):
                        if (depth_frame.get_distance(width,height) == 0):
                            to_change.append((width, height))
                            self.total = self.total +1
                            #print(width,height)
                        matrizDist[width][height]=depth_frame.get_distance(width,height)*10

            a = {}     
            vis = [False for i in range(0, len(to_change))]
            
            i = 0
            for values in to_change:
                d = []
                j=0
                
                if (vis[i]== False):
                    vis[i] = True
                    for vad in to_change:
                        if(vis[j]==False):
                            
                            if(abs(values[0] + values[1] - vad[0] - vad [1]) < 35):
                                vis[j]= True
                                d.append(vad)
                        j = j+1
                    a[values] = d
                    
                i = i +1
           
            val = []
            for key in a:
                
                val.append(self.BFS(matrizDist,key[0], key[1]))

            k = 0
            for key in a:
                for v in a[key]:
                    matrizDist[v[0]][v[1]] = val[k] 
                    matrizDist[key[0]][key[1]] = val[k]
                k = k +1    

            return matrizDist


        # Function to check if a cell
        # is be visited or not
        def isValid(self, row, col):
        
            # If cell lies out of bounds
            if (row < 0 or col < 0 or row >= self.width or col >= self.height):
                return False
        
            # If cell is already visited
            if (self.vis[row][col]):
                return False
        
            # Otherwise
            return True

        # Function to perform the BFS traversal
        def BFS(self,grid, row, col):
            self.vis = [[ False for i in range(self.height)] for j in range(self.width)]
            # Stores indices of the matrix cells
            q = queue()
        
            # Mark the starting cell as visited
            # and push it into the queue
            q.append(( row, col ))
            self.vis[row][col] = True
        
            # Iterate while the queue
            # is not empty
            while (len(q) > 0):
                cell = q.popleft()
                x = cell[0]
                y = cell[1]
                #print(grid[x][y], x, y)
        
                #q.pop()
        
                # Go to the adjacent cells
                for i in range(4):
                    adjx = x + self.dRow[i]
                    adjy = y + self.dCol[i]
                    if (self.isValid(adjx, adjy)):
                        if(grid[adjx][adjy]!=0):
                            self.total = self.total -1
                            
                            return grid[adjx][adjy]
                        else:    
                            q.append((adjx, adjy))
                            self.vis[adjx][adjy] = True

                




                
                
            
                

