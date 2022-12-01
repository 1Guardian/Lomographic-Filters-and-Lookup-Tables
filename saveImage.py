from imports import *

#================================================================
#
# Function: saveImage(image, extension, path, name)
#
# Description: This function is just a wrapper for the open cv
#              saving procedure since it has to be able to 
#              catch any opencv exceptions, and exception handling
#              in main makes it cluttered and hard to read.
#
# Returns: boolean | true on success, false on failure
#
#================================================================
def saveImage(image, extension, path, name):

    try:
        cv2.imwrite(path + '/' + name + extension, image)
    except Exception:
        print("Saving of the image file has failed Program will now exit.")
        sys.exit(-1)

    return True