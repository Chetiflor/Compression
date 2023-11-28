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
    blocks = []

    heigth, width = image.shape[:2]

    hPadding = heigth%8!=0 
    wPadding = width%8!=0

    numberOfBlocksInHeigth=heigth//8+hPadding
    numberOfBlocksInWidth=width//8+wPadding
 
    for kh in range(numberOfBlocksInHeigth):
        for kw in range(numberOfBlocksInWidth):
            currentBlock = np.zeros((8,8,1), np.uint8)
            currentBlock[:,:] = 127

            heigthRemainingOnEdge = 8 if kh!=numberOfBlocksInHeigth else heigth%8
            widthRemainingOnEdge = 8 if kw!= numberOfBlocksInWidth else width%8
            for i in range(heigthRemainingOnEdge):
                for j in range(widthRemainingOnEdge):
                    currentBlock[i,j] = image[kh*8+i,kw*8+j]

            blocks.append(currentBlock)
    return(blocks, numberOfBlocksInHeigth,numberOfBlocksInWidth)

def fuseBlocksIntoImage(blocks,numberOfBlocksInHeigth,numberOfBlocksInWidth):
    
    image = np.zeros((numberOfBlocksInHeigth*8,numberOfBlocksInWidth*8,1), np.uint8)
    for i in range(numberOfBlocksInHeigth):
        for j in range(numberOfBlocksInWidth):
            for ki in range(8):
                for kj in range(8):
                    image[i*8+ki,j*8+kj]=blocks[i*numberOfBlocksInWidth+j][ki,kj]
    return image

def dctOnImage(image,delta):
    blocks,numberOfBlocksInHeigth,numberOfBlocksInWidth = split(image)
    transformedBlocks=[]
    for i in range(len(blocks)):
        transformedBlocks.append(dct(blocks[i].astype(np.float32),delta))
    return (transformedBlocks,numberOfBlocksInHeigth,numberOfBlocksInWidth)

def idctOnBlocks(transformedBlocks,numberOfBlocksInHeigth,numberOfBlocksInWidth,delta):
    imageBlocks=[]
    for i in range(len(transformedBlocks)):
        imageBlocks.append(idct(transformedBlocks[i],delta))
    return fuseBlocksIntoImage(imageBlocks,numberOfBlocksInHeigth,numberOfBlocksInWidth)


# im = cv2.imread("images/01.png",0)

# delta=1/8

# blocks,heigth,width = dctOnImage(im,delta)
# imreco=idctOnBlocks(blocks,heigth,width,delta)

# plt.imshow(imreco,'gray')
# plt.colorbar()
# plt.show()



