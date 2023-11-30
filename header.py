import tools
import math 


def generateHeader(numberOfBlocksInHeight,numberOfBlocksInWidth,hPadding,wPadding,deltaScaled,sizeOfQuantifier,dictionary,firstMeanValue,debug=False):
    splitter = ""
    if(debug):
        splitter="|"
    header = ""

    header+=tools.int2bin(numberOfBlocksInHeight,8)
    header+=splitter
    header+=tools.int2bin(numberOfBlocksInWidth,8)
    header+=splitter
    header+=tools.int2bin(hPadding,3)
    header+=splitter
    header+=tools.int2bin(wPadding,3)
    header+=splitter  
    header+=tools.int2bin(deltaScaled,13)
    header+=splitter
    header+=tools.int2bin(sizeOfQuantifier-1,2)
    header+=splitter

    N = len(dictionary)
    header+=tools.pointedInt(N,4)
    header+=splitter

    symbols=[]
    codes=[]
    for x,y in dictionary.items():
        codes.append(x)
        symbols.append(y)

    minSymbols = min(symbols)
    maxSymbolsTranslated = max(symbols)-minSymbols
    
    if minSymbols<0:
        header+="1"
    else:
        header+="0"
    header+=splitter

    header+=tools.pointedInt(abs(minSymbols),4)
    header+=splitter


    
    sizeOfSymbols=len(tools.int2bin(maxSymbolsTranslated))
    header+=tools.pointedInt(sizeOfSymbols,4)
    header+=splitter

    maxSizeOfCode=len(max(codes, key=len))
    s_tmp=tools.pointedInt(maxSizeOfCode,4)
    sizeOfSizesOfCode=len(s_tmp)-4
    header+=s_tmp
    header+=splitter

    for i in range (N):
        header+=splitter
        header+=tools.int2bin(symbols[i]-minSymbols,sizeOfSymbols)
        header+=splitter
        header+=tools.int2bin(len(codes[i]),sizeOfSizesOfCode)
        header+=splitter
        header+=codes[i]
        header+=splitter

    header+=splitter    
    header+=tools.pointedInt(firstMeanValue,4)
    header+=splitter

    return header
    

def readHeader(wrappedStr):
    numberOfBlocksInHeight=tools.popInt(wrappedStr,8)
    numberOfBlocksInWidth=tools.popInt(wrappedStr,8)
    hPadding=tools.popInt(wrappedStr,3)
    wPadding=tools.popInt(wrappedStr,3)
    deltaScaled=tools.popInt(wrappedStr,13)
    delta = deltaScaled/(2**(7))
    sizeOfQuantifier=tools.popInt(wrappedStr,2)+1
    N=tools.popPointedInt(wrappedStr,4)
    signOfMin=tools.popInt(wrappedStr,1)
    minSymbols=tools.popPointedInt(wrappedStr,4)
    if (signOfMin==1):
        minSymbols*=-1
    sizeOfSymbols=tools.popPointedInt(wrappedStr,4)
    sizeOfSizesOfCode=len(tools.popPointedString(wrappedStr,4))
    dictionary={}
    for i in range(N):
        symbol=tools.popInt(wrappedStr,sizeOfSymbols)
        symbol+=minSymbols
        code=tools.popPointedString(wrappedStr,sizeOfSizesOfCode)
        dictionary[code]=symbol
    firstMeanValue=tools.popPointedInt(wrappedStr,4)
    return(numberOfBlocksInHeight,numberOfBlocksInWidth,hPadding,wPadding,delta,sizeOfQuantifier,dictionary,firstMeanValue)


    


