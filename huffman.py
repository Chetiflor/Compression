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
    dictionnaryEntries = generateDictionaryEntriesFromTreeRecursion(tree,"")
    dictionary = {}
    for i in range(len(dictionnaryEntries)):
        dictionary[dictionnaryEntries[i][1]]=dictionnaryEntries[i][0]
    return(dictionary)


symbols = [1,5,6,3,2,4,"stop"]
probabilities = [0.4,0.3,0.1,0.1,0.06,0.03,0]
tree = constTreeSort(symbolToObject(symbols),probabilities)
dico = generateDictionary(symbols,probabilities)

print(dico)

header = tools.generateHeader(64,64,0,0,2,dico,True)

print(header)