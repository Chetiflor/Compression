import tools

def symbolToObject(symbols):
    objects = []
    for i in range(len(symbols)):
        objects.append([symbols[i]])
    return objects

def treeSort(objects,probabilities):
    objectsNumber = len(objects)
    if objectsNumber==2:
        return objects
    newObject = [objects[objectsNumber-2],objects[objectsNumber-1]]
    newObjectProbability = probabilities[objectsNumber-2]+probabilities[objectsNumber-1]
    objects.pop()
    objects.pop()
    probabilities.pop()
    probabilities.pop()
    objects.append(newObject)
    probabilities.append(newObjectProbability)
    objectsNumber-=2
    while (probabilities[objectsNumber]>probabilities[objectsNumber-1] and objectsNumber>0):
        probabilities[objectsNumber],probabilities[objectsNumber-1]=probabilities[objectsNumber-1],probabilities[objectsNumber]
        objects[objectsNumber],objects[objectsNumber-1]=objects[objectsNumber-1],objects[objectsNumber]
        objectsNumber-=1
    return treeSort(objects,probabilities)

def constTreeSort(objects,probabilities):
    objects_tmp=objects.copy()
    probabilities_tmp=probabilities.copy()
    return(treeSort(objects_tmp,probabilities_tmp))

def generateDictionaryEntriesFromTreeRecursion(objects,currentCode):
    if len(objects)==1:
        return [[objects[0],currentCode]]
    return(generateDictionaryEntriesFromTreeRecursion(objects[0],currentCode+"0") + generateDictionaryEntriesFromTreeRecursion(objects[1],currentCode+"1"))
    
def generateDictionary(symbols,probabilities):
    tree = treeSort(symbolToObject(symbols),probabilities)
    dictionaryEntries = generateDictionaryEntriesFromTreeRecursion(tree,"")
    dictionary = {}
    for i in range(len(dictionaryEntries)):
        dictionary[dictionaryEntries[i][1]]=dictionaryEntries[i][0]
    return(dictionary)

def encode(listOfSymbols,dictionary):
    codeStr=""
    for i in range(len(listOfSymbols)):
        symbol=listOfSymbols[i]
        if symbol in dictionary.values():
            codeStr+=list(dictionary.keys())[list(dictionary.values()).index(symbol)]
        else:
            codeStr+=tools.ERROR
    return codeStr

def decode(wrappedStr,dictionary,numberOfSymbols):
    decodedList=[]
    maxSizeOfCode=len(max(dictionary.keys(), key=len))
    for i in range(numberOfSymbols):
        if (len(wrappedStr[0])==0):
            return([tools.ERROR])
        k=1
        while (k<=maxSizeOfCode and not(wrappedStr[0][:k] in dictionary)):
            k+=1
        if k>maxSizeOfCode:
            decodedList.append(tools.ERROR)
        else:
            key=tools.popString(wrappedStr,k)
            decodedList.append(dictionary[key])
    return decodedList



