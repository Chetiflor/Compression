import huffman
import block
import header
import runlength
import dct
import tools
import numpy as np

encodeWithFancyRange=False
encodeWithBodyMask=True

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

def generateBodyMask(body):
    mask=""
    for str in body:
        if (str=="00000"):
            mask+="1"
        else:
            mask+="0"
    return mask
        
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
    if(encodeWithBodyMask):
        body=[]
        for currentBlock in transformedBlocksList:
            body.append(block.encode(currentBlock,dictionary))
        mask=[generateBodyMask(body)]
        encodedMask=runlength.classicalRunLengthEncode(mask,6)
        encodedImageStr+=tools.pointedInt(len(encodedMask),4)
        encodedImageStr+=encodedMask
        for str in body:
            if str!="00000":
                encodedImageStr+=str
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
    if encodeWithBodyMask:
        sizeOfEncodedMask=tools.popPointedInt(wrappedEncodedImageStr,4)
        mask=[tools.popString(wrappedEncodedImageStr,sizeOfEncodedMask)]
        mask=runlength.classicalRunLengthDecode(mask,6)
        for i in range(len(mask)):
            if mask[i]=="1":
                zeros=["00000"]
                meanValue,currentBlock=block.decode(zeros,meanValue,dictionary)
                receivedBlocksList.append(currentBlock)
            else:
                meanValue,currentBlock=block.decode(wrappedEncodedImageStr,meanValue,dictionary)
                receivedBlocksList.append(currentBlock)
    else:
        while(wrappedEncodedImageStr[0]!=""):
            meanValue,currentBlock=block.decode(wrappedEncodedImageStr,meanValue,dictionary)
            receivedBlocksList.append(currentBlock)
    image=dct.dctBlocksToImage(receivedBlocksList,numberOfBlocksInHeight,numberOfBlocksInWidth,hPadding,wPadding,delta)
    return(image)





