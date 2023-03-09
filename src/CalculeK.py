

def CalculateK(matrizDist):
    col=len(matrizDist)
    fil=len(matrizDist[1]) 
    threshold=0.05
    values=set()
    for x in range (1, col):
            for y in range (1,fil):
                values.add(round(matrizDist[x-1][y-1]*10))


    print(values)

    return len(values)