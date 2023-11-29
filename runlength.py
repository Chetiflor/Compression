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

def encodeRange(wrappedStr,sizeOfQuantifier,debug=False):
    splitter = ""
    if(debug):
        splitter="|"

    encodedStr=""
    maxRunLength=2**(2**sizeOfQuantifier)
    while(wrappedStr[0]!=""):
        k=1
        bitValue=wrappedStr[0][0]
        while(k<len(wrappedStr[0]) and wrappedStr[0][k]==bitValue):
            k+=1
        lengthToPop=min(k,maxRunLength)
        binaryLength = tools.pointedVariable(lengthToPop,sizeOfQuantifier,1)
        encodedStr+=binaryLength
        encodedStr+=splitter
        tools.popString(wrappedStr,lengthToPop)
        k-=lengthToPop
        while(k>0):
            binaryLength = tools.pointedVariable(0,sizeOfQuantifier,1)
            encodedStr+=binaryLength
            encodedStr+=splitter
            tools.popString(wrappedStr,lengthToPop)
            lengthToPop=min(k,maxRunLength)
            binaryLength = tools.pointedVariable(lengthToPop,sizeOfQuantifier,1)
            encodedStr+=binaryLength
            encodedStr+=splitter
            tools.popString(wrappedStr,lengthToPop)
            k-=lengthToPop
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

def decodeRange(wrappedEncodedStr,sizeOfQuantifier):
    decodedStr=""
    bitValue="1"
    while(wrappedEncodedStr[0]!=""):
        strLength = tools.popPointedInt(wrappedEncodedStr,sizeOfQuantifier,1)
        decodedStr+=strLength*bitValue
        if bitValue=="1":
            bitValue="0"
        else:
            bitValue="1"

    return(decodedStr)

sizeOfQuantifier=3
myStr=["1111000000000000010111110111111111100000000000000"]
myEncodedStr=[encodeRange(myStr,sizeOfQuantifier)]
print(myEncodedStr[0])

print(decodeRange(myEncodedStr,sizeOfQuantifier))