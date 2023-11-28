import math

ERROR = "__ERROR__"

def int2bin(n,length=0,offset=0):
    s=""
    while (n>0):
        s=str(n%2)+s
        n=n//2
    if (length!=0 and len(s)>length):
        return ERROR
    while (len(s)<length):
        s="0"+s
    while (len(s)<offset):
        s="0"+s

    return s

def bin2int(str):
    n = 0
    length = len(str)
    for i in range(length):
        if (str[length-1-i]=="1"):
            n+=2**i
    return n


def pointedVariable(value,sizeOfPointer,offset=0):
    strVal=int2bin(value,offset=3)
    strSize=int2bin(max(len(strVal)-offset,0),sizeOfPointer)
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

def zigzag(height,width):
    indicesList=[]
    descending=False
    for k in range(height+width-1):
        indexOnDiagonal = [0,0]
        indexOnDiagonal[descending]=k
        while(indexOnDiagonal[0]>=0 and indexOnDiagonal[1]>=0):
            if(indexOnDiagonal[0]<height and indexOnDiagonal[1]<width):
                indicesList.append(indexOnDiagonal.copy())
            indexOnDiagonal[descending]-=1
            indexOnDiagonal[not(descending)]+=1
        descending=not(descending)
    return(indicesList)



def snake(height,width):
    indicesList=[]
    rightToLeft=False
    for i in range(height):
        for j in range(width):
            indicesList.append([i,j*(1-2*rightToLeft)+rightToLeft*(width-1)])
        rightToLeft=not(rightToLeft)
    return(indicesList)

def fillWithZeros(wrappedStr,expectedLength):
    lengthDifference=expectedLength-len(wrappedStr[0])
    if(lengthDifference>0):
        wrappedStr[0]+="0"*lengthDifference
    


    
            
