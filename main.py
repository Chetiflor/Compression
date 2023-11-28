import huffman
import header

symbols = [1,5,6,3,2,4]
probabilities = [0.4,0.3,0.1,0.1,0.06,0.03]
tree = huffman.constTreeSort(huffman.symbolToObject(symbols),probabilities)
dico = huffman.generateDictionary(symbols,probabilities)

print(dico)

myHeader = header.generateHeader(64,64,0,0,2,dico,129)
myHeaderDebug = header.generateHeader(64,64,0,0,2,dico,129,True)

# print(myHeaderDebug)
# wrappedStr=[myHeader+"11111"]
# print(header.readHeader(wrappedStr),wrappedStr[0])

example=[1,1,5,2,6,2,4,3,3]
str=huffman.encode(example,dico)
print(str)
print(huffman.decode([str],dico,len(example)))