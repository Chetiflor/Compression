import cv2
import numpy as np
import matplotlib.pyplot as plt

import compressor
import header
import tools

# symbols = [1,5,6,3,2,4]
# probabilities = [0.4,0.3,0.1,0.1,0.06,0.03]
# tree = huffman.constTreeSort(huffman.symbolToObject(symbols),probabilities)
# dico = huffman.generateDictionary(symbols,probabilities)

# print(dico)

# myHeader = header.generateHeader(64,64,0,0,2,dico,129)
# myHeaderDebug = header.generateHeader(64,64,0,0,2,dico,129,True)

# print(myHeaderDebug)
# wrappedStr=[myHeader+"11111"]
# print(header.readHeader(wrappedStr),wrappedStr[0])

# example=[1,1,5,2,6,2,4,3,3]
# str=huffman.encode(example,dico)
# print(str)
# print(huffman.decode([str],dico,len(example)))


im = cv2.imread("images/01.png",0)

height, width = im.shape[:2]

delta=1.2

encoded=compressor.encode(im,delta)
encodedDebug=compressor.encode(im,delta)
encodedImage=[encoded[0]]
encodedImageToFile=encodedImage.copy()
encodedImageDebug=[encodedDebug[0]]
lengthOfLine=50
print(8*height*width/len(encodedImage[0]))


if(True):
    with open("./encodedImage.txt", "w") as f:
        for i in range(len(encodedImageToFile[0])//lengthOfLine):
            f.write(tools.popString(encodedImageToFile,lengthOfLine))
            f.write('\n')
        f.write(encodedImageToFile[0])

imp1=im+1

transformedImage = compressor.decode(encodedImage)
err = np.sqrt(np.mean((np.square(cv2.subtract(im, transformedImage)))))
print(err)
cv2.imshow("compression",cv2.subtract(im, transformedImage))
cv2.waitKey(0)
cv2.destroyAllWindows()
