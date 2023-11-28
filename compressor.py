import huffman
import block
import header
import dct

def generateDictionaryFromBlocks(dctBlocksList):
    firstMeanValue=dctBlocksList[0][0][0]
    currentMeanValue=firstMeanValue
    error=0
    occurencesOfValues={}
    for currentBlock in dctBlocksList:
        error=currentBlock[0][0]-currentMeanValue
        currentMeanValue+=error
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
    transformedBlocksList,numberOfBlocksInHeight,numberOfBlocksInWidth=dct.dctOnImage(image,delta)
    hPadding=numberOfBlocksInHeight*8-height
    wPadding=numberOfBlocksInWidth*8-width
    dictionary,firstMeanValue=generateDictionaryFromBlocks(transformedBlocksList)
    print(dictionary)
    encodedImageStr+=header.generateHeader(numberOfBlocksInHeight,numberOfBlocksInWidth,hPadding,wPadding,delta,dictionary,firstMeanValue,debug)
    for currentBlock in transformedBlocksList:
        encodedImageStr+=splitter
        encodedImageStr+=block.encode(currentBlock,dictionary)
    return encodedImageStr,transformedBlocksList

def decode(wrappedEncodedImageStr):
    numberOfBlocksInHeight,numberOfBlocksInWidth,hPadding,wPadding,delta,dictionary,firstMeanValue=header.readHeader(wrappedEncodedImageStr)
    meanValue=firstMeanValue
    receivedBlocksList=[]
    while(wrappedEncodedImageStr[0]!=""):
        error,currentBlock=block.decode(wrappedEncodedImageStr,meanValue,dictionary)
        meanValue+=error
        currentBlock[0][0]=meanValue
        receivedBlocksList.append(currentBlock)
    return(receivedBlocksList)





