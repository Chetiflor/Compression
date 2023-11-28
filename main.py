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

encoded=compressor.encode(im,1)
encodedDebug=compressor.encode(im,1,True)
encodedImage=[encoded[0]]
encodedImageDebug=[encodedDebug[0]]
lengthOfLine=50
print(8*height*width/len(encodedImage[0]))


if(True):
    with open("./encodedImage.txt", "w") as f:
        for i in range(len(encodedImageDebug[0])//lengthOfLine):
            f.write(tools.popString(encodedImageDebug,lengthOfLine))
            f.write('\n')
        f.write(encodedImageDebug[0])

print(compressor.decode(encodedImage))