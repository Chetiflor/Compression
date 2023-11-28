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


def decode(wrappedEncodedStr,sizeOfQuantifier,expectedNumberOfOnes):
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

# myStr="11110001011111011111100000000000"
# myEncodedStr=encode([myStr],3)

# print(decode([myEncodedStr],3,16))