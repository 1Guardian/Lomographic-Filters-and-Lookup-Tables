from imports import *

#================================================================
#
# Function: changeVinnete(img, eye):
#
# Description: This function takes in an image and a value
#              and uses the distance from the center of the 
#              image to the border, and applies a fading 
#              vignette to the image with the 'eye' being
#              controlled by the input variable 
#
# Returns: modified image
#
#================================================================
def changeVinnete(img, eye):

    #set eye
    eye = eye/2

    #get the shape of the input image
    x, y = img.shape[:2]

    #get image to modify
    modified = np.copy(img)

    #store variables because I'm lazy
    centerX = np.floor(x/2)
    centerY = np.floor(y/2)

    #find percent of image that should be unaffected
    eyeDecimal = eye/100

    #get boundaries
    maxX = np.floor(x * eyeDecimal)
    maxY = np.floor(y * eyeDecimal)
    maxDistance = np.linalg.norm(np.array((centerX, centerY)) - np.array((maxX, maxY)))

    #find maximum distance
    absoluteDistance = np.linalg.norm(np.array((x ,y)) - np.array((centerX, centerY)))

    #take every pixel and calculate the euclidean distance, putting each one through
    #our vignette lut/kernel function
    for i in range(x-1):
        for j in range(y-1):
            currentDistance = (np.linalg.norm(np.array((i ,j)) - np.array((centerX, centerY))) - maxDistance)
            if (currentDistance > 0):
                modified[i,j] = (1 - ( currentDistance / (absoluteDistance- maxDistance))) * modified[i,j]
                

    return modified