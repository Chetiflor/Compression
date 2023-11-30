import huffman
import block
import header
import runlength
import dct
import numpy as np

encodeWithFancyRange=True

def generateDictionaryAndComputeError(dctBlocksList):
    firstMeanValue=dctBlocksList[0][0][0]
    currentMeanValue=firstMeanValue
    error=0
    occurencesOfValues={}
    for currentBlock in dctBlocksList:
        error=currentBlock[0][0]-currentMeanValue
        currentMeanValue=currentBlock[0][0]
        currentBlock[0][0]=error
        for line in currentBlock:
            for value in line:
                if value!=0:
                    if value in occurencesOfValues:
                        occurencesOfValues[value]+=1
                    else:
                        occurencesOfValues[value]=1
    dictionary = huffman.generateDictionary(list(occurencesOfValues.keys()),list(occurencesOfValues.values()))
    return(dictionary,firstMeanValue)
        
def encode(image,delta,sizeOfQuantifier,sizeOfMinRange=0,debug=False):
    splitter = ""
    if(debug):
        splitter="_"

    encodedImageStr=""
    height,width=image.shape[:2]    
    deltaScaled=int(np.round(delta*(2**(7))))

    transformedBlocksList,numberOfBlocksInHeight,numberOfBlocksInWidth=dct.dctBlocksFromImage(image,delta)
    hPadding=numberOfBlocksInHeight*8-height
    wPadding=numberOfBlocksInWidth*8-width
    dictionary,firstMeanValue=generateDictionaryAndComputeError(transformedBlocksList)
    encodedImageStr+=header.generateHeader(numberOfBlocksInHeight,numberOfBlocksInWidth,hPadding,wPadding,deltaScaled,sizeOfQuantifier,dictionary,firstMeanValue,debug)
    if(encodeWithFancyRange):
        body=[""]
        for currentBlock in transformedBlocksList:
            body[0]+=splitter
            body[0]+=block.encode(currentBlock,dictionary)
        encodedImageStr+=runlength.encodeRangeFancy(body,sizeOfQuantifier,sizeOfMinRange)
        return [encodedImageStr]    
    for currentBlock in transformedBlocksList:
        encodedImageStr+=splitter
        encodedImageStr+=block.encode(currentBlock,dictionary)
    return [encodedImageStr]

def decode(wrappedEncodedImageStr):
    numberOfBlocksInHeight,numberOfBlocksInWidth,hPadding,wPadding,delta,sizeOfQuantifier,dictionary,meanValue=header.readHeader(wrappedEncodedImageStr)
    if encodeWithFancyRange:
        wrappedEncodedImageStr=[runlength.decodeRangeFancy(wrappedEncodedImageStr,sizeOfQuantifier)]
    receivedBlocksList=[]
    while(wrappedEncodedImageStr[0]!=""):
        meanValue,currentBlock=block.decode(wrappedEncodedImageStr,meanValue,dictionary)
        receivedBlocksList.append(currentBlock)
    image=dct.dctBlocksToImage(receivedBlocksList,numberOfBlocksInHeight,numberOfBlocksInWidth,hPadding,wPadding,delta)
    return(image)





