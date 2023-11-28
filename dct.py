import cv2
import numpy as np
import matplotlib.pyplot as plt

Z=np.array([[16,11,10,16,24,40,51,61],
 [12,12,14,19,26,58,60,55],
 [14,13,16,24,40,57,69,56],
 [14,17,22,29,51,87,80,62],
 [18,22,37,56,68,109,103,77],
 [24,35,55,64,81,104,113,92],
 [49,64,78,87,103,121,120,101],
 [72,92,95,98,112,100,103,99]
])

def dct(block,delta):
    return np.trunc(np.divide(cv2.dct((block)),(1/delta)*Z))

def idct(block,delta):
    idctValues = cv2.idct(np.multiply(block,(1/delta)*Z))
    idctValues[idctValues<0]=0
    return(idctValues)


def split(image):
    blocksList = []

    height, width = image.shape[:2]

    hPadding = height%8!=0 
    wPadding = width%8!=0

    numberOfBlocksInHeight=height//8+hPadding
    numberOfBlocksInWidth=width//8+wPadding
 
    for kh in range(numberOfBlocksInHeight):
        for kw in range(numberOfBlocksInWidth):
            currentBlock = np.zeros((8,8,1), np.uint8)
            currentBlock[:,:] = 127

            heightRemainingOnEdge = 8 if kh!=numberOfBlocksInHeight else height%8
            widthRemainingOnEdge = 8 if kw!= numberOfBlocksInWidth else width%8
            for i in range(heightRemainingOnEdge):
                for j in range(widthRemainingOnEdge):
                    currentBlock[i,j] = image[kh*8+i,kw*8+j]

            blocksList.append(currentBlock)
    return(blocksList, numberOfBlocksInHeight,numberOfBlocksInWidth)

def fuseBlocksIntoImage(blocksList,numberOfBlocksInHeight,numberOfBlocksInWidth):
    
    image = np.zeros((numberOfBlocksInHeight*8,numberOfBlocksInWidth*8,1), np.uint8)
    for i in range(numberOfBlocksInHeight):
        for j in range(numberOfBlocksInWidth):
            for ki in range(8):
                for kj in range(8):
                    image[i*8+ki,j*8+kj]=blocksList[i*numberOfBlocksInWidth+j][ki,kj]
    return image

def dctOnImage(image,delta):
    blocksList,numberOfBlocksInHeight,numberOfBlocksInWidth = split(image)
    transformedBlocksList=[]
    for i in range(len(blocksList)):
        transformedBlocksList.append(list(dct(blocksList[i].astype(np.float32),delta).astype(int)))
    return (transformedBlocksList,numberOfBlocksInHeight,numberOfBlocksInWidth)

def idctOnBlocks(transformedBlocksList,numberOfBlocksInHeight,numberOfBlocksInWidth,delta):
    imageBlocksList=[]
    for i in range(len(transformedBlocksList)):
        imageBlocksList.append(idct(transformedBlocksList[i],delta))
    return fuseBlocksIntoImage(imageBlocksList,numberOfBlocksInHeight,numberOfBlocksInWidth)






