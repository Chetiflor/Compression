import tools

def encode(wrappedStr,sizeOfQuantifier,cutEndZeros=True,debug=False):
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


def decode(wrappedEncodedStr,sizeOfQuantifier):
    decodedStr=""
    while(wrappedEncodedStr[0]!=""):
        chunk = tools.popString(wrappedEncodedStr,sizeOfQuantifier+1)
        decodedStr+=(tools.bin2int(chunk[:sizeOfQuantifier])+1)*chunk[-1]
    return(decodedStr)

