import tools

def encodePositions(wrappedStr,sizeOfQuantifier,cutEndZeros=True,debug=False):
    splitter = ""
    if(debug):
        splitter="|"

    encodedStr=""
    maxRunLength=2**sizeOfQuantifier
    while(wrappedStr[0]!=""):
        k=1
        bitValue=wrappedStr[0][0]
        while(k<len(wrappedStr[0]) and wrappedStr[0][k]==bitValue):
            k+=1
        if(cutEndZeros and k==len(wrappedStr[0]) and bitValue=="0"):
            break
        while(k>0):
            lengthToPop=min(k,maxRunLength)
            binaryLength = tools.int2bin(lengthToPop-1,sizeOfQuantifier)
            encodedStr+=binaryLength+bitValue
            encodedStr+=splitter
            tools.popString(wrappedStr,lengthToPop)
            k-=lengthToPop
    return(encodedStr)

def encodePositionsQuantifier(wrappedStr,sizeOfQuantifier,cutEndZeros=False,debug=False):
    splitter = ""
    if(debug):
        splitter="|"

    encodedStr=""
    maxRunLength=2**(2**sizeOfQuantifier)-1
    while(wrappedStr[0]!=""):
        k=1
        bitValue=wrappedStr[0][0]
        while(k<len(wrappedStr[0]) and wrappedStr[0][k]==bitValue):
            k+=1
        if(cutEndZeros and k==len(wrappedStr[0]) and bitValue=="0"):
            break
        lengthToPop=min(k,maxRunLength)
        binaryLength = tools.pointedInt(lengthToPop,sizeOfQuantifier,offset=1)
        encodedStr+=binaryLength
        encodedStr+=splitter
        tools.popString(wrappedStr,lengthToPop)
        k-=lengthToPop
        while(k>0):
            binaryLength = tools.pointedInt(0,sizeOfQuantifier,offset=1)
            encodedStr+=binaryLength
            encodedStr+=splitter
            lengthToPop=min(k,maxRunLength)
            binaryLength = tools.pointedInt(lengthToPop,sizeOfQuantifier,offset=1)
            encodedStr+=binaryLength
            encodedStr+=splitter
            tools.popString(wrappedStr,lengthToPop)
            k-=lengthToPop
    return(encodedStr)

def checkIfConstantRange(wrappedStr,startingPosition,rangeToSearch):

    for i in range(rangeToSearch):
        if startingPosition+i<len(wrappedStr[0]):
            if wrappedStr[0][startingPosition+i]!=wrappedStr[0][startingPosition]:
                return False
    return True

def getNextStringIntOrString(wrappedStr,sizeOfQuantifier,sizeOfMinRange):
    k=0
    maxHeterogeneousStringLength = 2**(2**(sizeOfQuantifier+1))-1
    maxRangeLength=2**(2**sizeOfQuantifier-1)-1+sizeOfMinRange
    while (not(checkIfConstantRange(wrappedStr,k,sizeOfMinRange)) and k<maxHeterogeneousStringLength):
        k+=1
    if k!=0:
        return(False,tools.popString(wrappedStr,k))
    while (k<maxRangeLength-sizeOfMinRange and k+sizeOfMinRange<len(wrappedStr[0]) and wrappedStr[0][k+sizeOfMinRange]==wrappedStr[0][0]):
        k+=1
    return(True,tools.popString(wrappedStr,k+sizeOfMinRange))

def estimateSizeOfRentableRange(sizeOfQuantifier):
    k=sizeOfQuantifier+3
    while 2**(k-(sizeOfQuantifier+2))-k<0: 
        k+=1
    return k

def encodeRangeFancy(wrappedStr,sizeOfQuantifier,sizeOfMinRange=0,debug=False):
    splitter = ""
    if(debug):
        splitter="|"
    encodedStr=""
    if sizeOfMinRange==0:
        sizeOfMinRange=estimateSizeOfRentableRange(sizeOfQuantifier)
    maxRangeLength=2**(2**sizeOfQuantifier-1)
    while(wrappedStr[0]!=""):
        bitValue=wrappedStr[0][0]
        isInt,str=getNextStringIntOrString(wrappedStr,sizeOfQuantifier,sizeOfMinRange)
        if(not(isInt)):
            encodedStr+="0"+tools.pointedInt(len(str)-1,sizeOfQuantifier+1,1)
            encodedStr+=splitter   
            encodedStr+=splitter
            encodedStr+=str
            encodedStr+=splitter
        else:
            lengthStr=len(str)
            rangeSizeToEncode=min(maxRangeLength,lengthStr)
            rangeSizeEncoded=tools.int2bin(rangeSizeToEncode-1,minimalLength=1)
            lengthNumberToEncode=len(rangeSizeEncoded)
            quantifierValue=tools.int2bin(lengthNumberToEncode,sizeOfQuantifier)
            encodedStr+="1"+quantifierValue+bitValue
            encodedStr+=splitter   
            encodedStr+=splitter            
            encodedStr+=rangeSizeEncoded
            encodedStr+=splitter
            lengthStr-=maxRangeLength
            while lengthStr>0:
                rangeSizeToEncode=min(maxRangeLength,lengthStr)
                rangeSizeEncoded=tools.int2bin(rangeSizeToEncode-1,minimalLength=1)
                lengthNumberToEncode=len(rangeSizeEncoded)
                quantifierValue=tools.int2bin(lengthNumberToEncode,sizeOfQuantifier)
                encodedStr+="1"+quantifierValue+bitValue
                encodedStr+=splitter   
                encodedStr+=splitter            
                encodedStr+=rangeSizeEncoded
                encodedStr+=splitter
                lengthStr-=rangeSizeToEncode
    return(encodedStr)


def decodePositions(wrappedEncodedStr,sizeOfQuantifier,expectedNumberOfOnes):
    decodedStr=""
    onesCount=0
    while(wrappedEncodedStr[0]!="" and onesCount<expectedNumberOfOnes):
        chunk = tools.popString(wrappedEncodedStr,sizeOfQuantifier+1)
        bitValue=chunk[-1]
        strLength=tools.bin2int(chunk[:sizeOfQuantifier])+1
        if(bitValue=="1"):
            onesCount+=strLength
        decodedStr+=strLength*bitValue
    return(decodedStr)

def decodePosistionsQuantifier(wrappedEncodedStr,sizeOfQuantifier,expectedNumberOfOnes=0,countOnes=False):
    decodedStr=""
    bitValue="1"
    onesCount=0
    while(wrappedEncodedStr[0]!="" and (not(countOnes) or (countOnes and onesCount<expectedNumberOfOnes))):
        strLength = tools.popPointedInt(wrappedEncodedStr,sizeOfQuantifier,1)
        if(bitValue=="1"):
            onesCount+=strLength
        decodedStr+=strLength*bitValue
        if bitValue=="1":
            bitValue="0"
        else:
            bitValue="1"

    return(decodedStr)

def decodeRangeFancy(wrappedEncodedStr,sizeOfQuantifier):
    decodedStr=""
    while(wrappedEncodedStr[0]!=""):
        valueType = tools.popString(wrappedEncodedStr,1)
        if(valueType=="0"):
            lengthStr=tools.popPointedInt(wrappedEncodedStr,sizeOfQuantifier+1,1)+1
            decodedStr+=tools.popString(wrappedEncodedStr,lengthStr)
        if valueType=="1":
            sizeOfRangeSize=tools.popInt(wrappedEncodedStr,sizeOfQuantifier)
            bitValue=tools.popString(wrappedEncodedStr,1)
            rangeSize=tools.popInt(wrappedEncodedStr,sizeOfRangeSize)+1
            decodedStr+=rangeSize*bitValue
    return(decodedStr)

# sizeOfQuantifier=3
# sizeOfMinRange=3
# myStr=["1111000000000000010111110111111111100000000000000"]
# myEncodedStr=[encodeRangeFancy(myStr.copy(),sizeOfQuantifier,sizeOfMinRange)]
# myEncodedStrDebug=[encodeRangeFancy(myStr.copy(),sizeOfQuantifier,sizeOfMinRange,debug=True)]
# print(myEncodedStrDebug[0])
# print(myStr[0])

# print(decodeRangeFancy(myEncodedStr,sizeOfQuantifier))