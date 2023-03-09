

def CalculateK(matrizDist):
    col=len(matrizDist)
    fil=len(matrizDist[1]) 
    threshold=0.05
    values=[]
    for x in range (1, col):
            for y in range (1,fil):
                  if(x==1 and y==1):
                       values.append(matrizDist[x][y])
                  for value in range(1,8):
                    print("LLorando")
                    if(matrizDist[x][y]>values[value]+threshold or matrizDist[x][y]<values[value]-threshold):
                        values.append(matrizDist[x][y])
    return len(values)