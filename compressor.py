import huffman
import block
import header
import dct

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
        
def encode(image,delta,debug=False):
    splitter = ""
    if(debug):
        splitter="_"

    encodedImageStr=""
    height,width=image.shape[:2]    
    deltaScaled= round((delta-1)*header.deltaRangeSize+2**(header.deltaRangeSize-1))
    delta=1+(deltaScaled-2**(header.deltaRangeSize-1))/header.deltaRangeSize

    transformedBlocksList,numberOfBlocksInHeight,numberOfBlocksInWidth=dct.dctBlocksFromImage(image,delta)
    hPadding=numberOfBlocksInHeight*8-height
    wPadding=numberOfBlocksInWidth*8-width
    dictionary,firstMeanValue=generateDictionaryAndComputeError(transformedBlocksList)
    encodedImageStr+=header.generateHeader(numberOfBlocksInHeight,numberOfBlocksInWidth,hPadding,wPadding,deltaScaled,dictionary,firstMeanValue,debug)
    for currentBlock in transformedBlocksList:
        encodedImageStr+=splitter
        encodedImageStr+=block.encode(currentBlock,dictionary)
    return encodedImageStr,transformedBlocksList

def decode(wrappedEncodedImageStr):
    numberOfBlocksInHeight,numberOfBlocksInWidth,hPadding,wPadding,delta,dictionary,meanValue=header.readHeader(wrappedEncodedImageStr)
    receivedBlocksList=[]
    while(wrappedEncodedImageStr[0]!=""):
        meanValue,currentBlock=block.decode(wrappedEncodedImageStr,meanValue,dictionary)
        receivedBlocksList.append(currentBlock)
    image=dct.dctBlocksToImage(receivedBlocksList,numberOfBlocksInHeight,numberOfBlocksInWidth,hPadding,wPadding,delta)
    return(image)





