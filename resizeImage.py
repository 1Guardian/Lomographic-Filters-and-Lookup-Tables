from imports import *

#================================================================
#
# Function: resizeImage(image, x, y, metaData)
#
# Description: This function is pretty simple, it takes in the
#              the arguments passed from the command line and 
#              resizes the images to fit within the confines 
#              specfied. 
#
# Returns: resizedImg | type: openCV image 
#    OR
# Returns: image | original image unchanged
#
#================================================================
def resizeImage(image, x, y, metaData):

    #variables to control decision making
    biggerX = False
    biggerY = False

    #check to see if image needs to be resized at all
    if (metaData.get("sizeX") > x):
        biggerX = True
    if (metaData.get("sizeY") > y):
        biggerX = True

    #deal with posibility that both exceed specified bounds
    #method: compare sizes and take the larger one
    if (biggerX == True == biggerY):
        biggerX = metaData.get("sizeX") > metaData.get("sizeY")
        biggerY = metaData.get("sizeX") < metaData.get("sizeY")

    if(biggerX):

        #get multiplying factor
        delta = metaData.get("sizeX") / x

        print(delta)

        #scale the image 
        newSize = (math.floor(metaData.get("sizeX") / delta), math.floor(metaData.get("sizeY") / delta))

        try:
            resizedImg = cv2.resize(image, newSize)
        except Exception:
            print("Scaling the image file for the window has failed; Program will now exit.")
            sys.exit(-1)
            
        #return image
        return resizedImg

    elif(biggerY):

        #get multiplying factor
        delta = metaData.get("sizeY") / y

        #scale the image 
        newSize = (math.floor(metaData.get("sizeX") / delta), math.floor(metaData.get("sizeY") / delta))

        try:
            resizedImg = cv2.resize(image, newSize)
        except Exception:
            print("Scaling the image file for the window has failed; Program will now exit.")
            sys.exit(-1)
        
        #return image
        return resizedImg
    
    #else, image fit, exit
    return image