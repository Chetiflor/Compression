import cv2
import numpy as np
import matplotlib.pyplot as plt

import compressor
import runlength
import tools

im = cv2.imread("images/01.png",0)
height, width = im.shape[:2]

##############################
### Paramètres d'affichage ###
##############################

debug=False
toFile=False
printReconstruction=True
printError=True
gaussianBlur=True
kernelSize=3

#############################
### Paramètres d'encodage ###
#############################
# Le paramètre de compression n'est pas directement le taux,
# il permet seulement de le moduler mais n'a pas de signification

compressionParameter=1.11
sizeOfQuantifier=3
sizeOfMinRange=27

###########################
### Encodage - Décodage ###
###########################
# Le paramètre de compression n'est pas directement le taux,


encoded=compressor.encode(im,compressionParameter,3,sizeOfMinRange)
encodedImageToFile=encoded.copy()
compressionFactor=8*height*width/len(encoded[0])
transformedImage = compressor.decode(encoded)
meanSquareErrorWithoutGaussianBlur = np.sqrt(np.mean((np.square(cv2.subtract(im, transformedImage)))))

##################
### Affichages ###
##################

print("Taux de compression: ",compressionFactor)
print("Erreur moyenne: ",meanSquareErrorWithoutGaussianBlur)

if gaussianBlur:
    kernel = np.ones((kernelSize,kernelSize),np.float32)/(kernelSize**2)
    transformedImage = cv2.GaussianBlur(transformedImage,(kernelSize,kernelSize),1)
    meanSquareErrorWithGaussianBlur = np.sqrt(np.mean((np.square(cv2.subtract(im, transformedImage)))))
    print("Erreur moyenne après lissage: ",meanSquareErrorWithGaussianBlur)

if(debug):
    encodedImageToFile=compressor.encode(im,compressionParameter,3,sizeOfMinRange)

if(toFile):
    lengthOfLine=50
    with open("./encodedImage.txt", "w") as f:
        for i in range(len(encodedImageToFile[0])//lengthOfLine):
            f.write(tools.popString(encodedImageToFile,lengthOfLine))
            f.write('\n')
        f.write(encodedImageToFile[0])

if printError:
    cv2.imshow("Erreur",cv2.subtract(im, transformedImage))
if printReconstruction:
    cv2.imshow("Image apres compression",transformedImage)

cv2.waitKey(0)
cv2.destroyAllWindows()
