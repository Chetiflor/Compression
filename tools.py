ERROR = "error"

def int2bin(n,length=0):
    s=""
    while (n!=0):
        s=str(n%2)+s
        n=n//2
    if (length!=0 and len(s)>length):
        return ERROR
    while (len(s)<length):
        s="0"+s
    return s

def bin2int(str):
    n = 0
    length = len(str)
    for i in range(length):
        if (str[length-1-i]=="1"):
            n+=2^i
    return n


def pointedVariable(value,sizeOfPointer):
    strVal=int2bin(value)
    strSize=int2bin(len(strVal),sizeOfPointer)
    if (strSize!=ERROR):
        return(strSize+strVal)
    return(ERROR)

def generateHeader(hBlocks,wBlocks,hPadding,wPadding,delta,dictionary,debug=False):
    splitter = ""
    if(debug):
        splitter="|"
    header = ""

    header+=int2bin(hBlocks,8)
    header+=splitter
    header+=int2bin(wBlocks,8)
    header+=splitter
    header+=int2bin(hPadding,3)
    header+=splitter
    header+=int2bin(wPadding,3)
    header+=splitter

    N = len(dictionary)
    header+=pointedVariable(N,4)
    header+=splitter

    symbols=[]
    codes=[]
    stopCode=""
    for x,y in dictionary.items():
        if (y!="stop"):
            codes.append(x)
            symbols.append(y)
        else:
            stopCode=x

    minSymbols = min(symbols)
    if minSymbols<0:
        header+="1"
        minSymbols*=-1
    else:
        header+="0"
    header+=splitter

    header+=pointedVariable(minSymbols,4)
    header+=splitter

    for s in symbols:
        s-=minSymbols

    
    maxSymbols = max(symbols)
    sizeOfSymbols=len(int2bin(maxSymbols))
    header+=pointedVariable(sizeOfSymbols,4)
    header+=splitter

    maxSizeOfCode=len(max(codes, key=len))
    s_tmp=pointedVariable(maxSizeOfCode,4)
    sizeOfSizesOfCode=len(s_tmp)-4
    header+=s_tmp
    header+=splitter

    for i in range (N-1):
        header+=splitter
        header+=int2bin(symbols[i],sizeOfSymbols)
        header+=splitter
        header+=int2bin(len(codes[i]),sizeOfSizesOfCode)
        header+=splitter
        header+=codes[i]
        header+=splitter

    header+=splitter
    header+=int2bin(len(stopCode),sizeOfSizesOfCode)
    header+=splitter
    header+=stopCode
    return header
    


