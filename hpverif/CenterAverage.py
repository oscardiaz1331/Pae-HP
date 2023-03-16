def centerAverage(matrizDist,rangeWidth,rangeHeight):
    media = 0
    pix = 0
    col=len(matrizDist)
    fil=len(matrizDist[1])
    for x in range (int((col/2)-rangeWidth), int((col/2)+rangeWidth)):
            for y in range ((int(fil)-rangeHeight), int((fil/2)+rangeHeight)):
                    media +=  matrizDist[x][y]
                    pix+=1
    media = media/pix
    return media