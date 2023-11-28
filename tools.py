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
            n+=2**i
    return n


def pointedVariable(value,sizeOfPointer):
    strVal=int2bin(value)
    strSize=int2bin(len(strVal),sizeOfPointer)
    if (strSize!=ERROR):
        return(strSize+strVal)
    return(ERROR)

def popString(wrappedStr,sizeOfPop):
    pop=wrappedStr[0][:sizeOfPop]
    wrappedStr[0]=wrappedStr[0][sizeOfPop:]
    return(pop)

def popPointedString(wrappedStr,sizeOfPointer):
    ptr=popString(wrappedStr,sizeOfPointer)
    sizeOfVariable = bin2int(ptr)
    return(popString(wrappedStr,sizeOfVariable))

def popInt(wrappedStr,sizeOfPop):
    return(bin2int(popString(wrappedStr,sizeOfPop)))

def popPointedInt(wrappedStr,sizeOfPointer):
    return(bin2int(popPointedString(wrappedStr,sizeOfPointer)))


            
