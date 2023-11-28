import tools
import huffman
import runlength

sizeOfRunlengthQuantifier=3

def generateStartingHuffmanMarker(numberOfValues):
    marker=tools.pointedVariable(numberOfValues,2,3)
    return(marker)

def readNumberOfValuesFromHuffmanMarker(wrappedMarker):
    sizeOfNumberOfValues=tools.popInt(wrappedMarker,2)+3
    return(tools.popInt(wrappedMarker,sizeOfNumberOfValues))

def encode(dct88Block,previousMeanValue,dictionary):
    encodedBlock=""
    currentMeanValue=dct88Block[0,0]
    dct88Block[0,0]=currentMeanValue-previousMeanValue
    indicesRoute=tools.zigzag(8,8)
    runlengthToEncode=""
    valuesToEncode=[]
    for [x,y] in indicesRoute:
        currentValue=dct88Block[x][y]
        if(currentValue==0):
            runlengthToEncode+="0"
        else:
            runlengthToEncode+="1"
            valuesToEncode.append(currentValue)
    encodedBlock+=generateStartingHuffmanMarker(len(valuesToEncode))
    encodedBlock+=huffman.encode(valuesToEncode,dictionary)
    encodedBlock+=runlength.encode([runlengthToEncode],sizeOfRunlengthQuantifier)

    return encodedBlock

def decode(wrappedStr,previousMeanValue,dictionary):
    decodedValuesList=[[0 for i in range(8)] for j in range(8)]
    numberOfValues=readNumberOfValuesFromHuffmanMarker(wrappedStr)
    values=huffman.decode(wrappedStr,dictionary,numberOfValues)
    values[0]+=previousMeanValue
    valuesPositionsMask=runlength.decode(wrappedStr,sizeOfRunlengthQuantifier)
    tools.fillWithZeros([valuesPositionsMask],64)
    indicesRoute=tools.zigzag(8,8)
    k=0
    for i in range(64):
        if(valuesPositionsMask[i]=="1"):
            decodedValuesList[indicesRoute[i]]=values[k]
            k+=1
    return(values[0],decodedValuesList)
        
