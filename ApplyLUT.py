from imports import *
#================================================================
#
# Function: LUT(value):
#
# Description: This function actually calculates each value when called
#
# Returns: new value from table
#
#================================================================
def LUT(value):

    LookUpTable = []

    for i in range(256):

        #build the LUT
        LookUpTable.append(int((256)/(1 + pow(math.e, (-((i/256)-0.5))/value))))
    
    return LookUpTable


#================================================================
#
# Function: applyRedLut(image, value):
#
# Description: This function takes in an image and a value
#              and applies a LUT on the red channel based on the
#              value that is given
#
# Returns: modified image
#
#================================================================
def applyRedLut(image, value):
    
    #global variables to work with
    imageAsArray = np.copy(image)
    LookUpTable = LUT(value)

    #loop over image and remap all the red channels to their new values
    #NOTE: BGR -> red is the last value
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            image[x,y, 2] = LookUpTable[image[x,y, 2]]

    return image

#================================================================
#
# Function: applyGreenLut(image, value):
#
# Description: This function takes in an image and a value
#              and applies a LUT on the green channel based on the
#              value that is given
#
# Returns: modified image
#
#================================================================
def applyGreenLut(image, value):
    
    #global variables to work with
    imageAsArray = np.copy(image)
    LookUpTable = LUT(value)

    #loop over image and remap all the green channels to their new values
    #NOTE: BGR -> green is the second value
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            image[x,y, 1] = LookUpTable[image[x,y, 1]]

    return image

#================================================================
#
# Function: applyBlueLut(image, value):
#
# Description: This function takes in an image and a value
#              and applies a LUT on the blue channel based on the
#              value that is given
#
# Returns: modified image
#
#================================================================
def applyBlueLut(image, value):
    
    #global variables to work with
    imageAsArray = np.copy(image)
    LookUpTable = LUT(value)

    #loop over image and remap all the blue channels to their new values
    #NOTE: BGR -> blue is the first value
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            image[x,y, 0] = LookUpTable[image[x,y, 0]]

    return image