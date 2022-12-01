from imports import *

#================================================================
#
# Function: haloVignette(img, eye, fixed):
#
# Description: This function takes in an image and a value
#              and creates a mask of 3 channels, with each
#              channel getting a radius of 'unaffected' area
#              which is set by the input variable
#
# Returns: modified image
#
#================================================================
def haloVignette(img, eye, fixed):

    #prevent division by zero for the blur function
    if eye <= 0:
        eye = 1

    #get the percent of the radius as given by 'eye'    
    percent = eye/100

    #get the shape of the input image
    sizex, sizey = img.shape[:2]

    #make our mask
    mask = np.full((sizex, sizey, img.shape[2]), 0.75)
    centerX = int(sizex / 2)
    centerY = int(sizey / 2)

    #get image to modify
    modified = np.copy(img)

    #create the circle of unaffected pixels
    r = int((min(sizex, sizey) * percent)/2)

    #make circle in mask
    for i in range(3):
        for x in range(sizex):
            for y in range(sizey):
                if (np.linalg.norm(np.array((x ,y)) - np.array((centerX, centerY))) < r):
                     mask[x,y,i] = 1
    
    #blur
    if fixed:
        mask = cv2.blur(mask, (100,100)) 
    else:
        mask = cv2.blur(mask, (r,r)) 

    #apply mask
    for i in range(3):
        modified[:,:,i] = modified[:,:,i] * mask[:,:,i]; 

    return modified

