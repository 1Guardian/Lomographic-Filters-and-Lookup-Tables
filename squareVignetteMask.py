from imports import *

#================================================================
#
# Function: squareVignette(img, eye):
#
# Description: This function takes in an image and a value
#              and creates a 2D mask using a constant decrease
#              from 1 to 0 across the pixels, forming a box-like
#              vignette which increases the blacks as the eye
#              tightens
#
# Returns: modified image
#
#================================================================
def squareVignette(img, eye):

    #get the shape of the input image
    y, x = img.shape[:2]

    #which img dimension is larger
    larger = (x > y) * x + (y >= x) * y

    #make array of half of height or width of
    #image based on which is larger
    arr = np.arange(larger/2)
    arr = arr / (larger/2)

    #fill rest of array with mirror of array
    brr = np.flip(arr)

    #make final image array
    crr = np.concatenate((arr, brr))

    #make matrix
    mask = np.zeros([y,x],dtype='float')

    #get the starting points for both dimensions
    x_start = math.ceil((larger - x)/2)
    y_start = math.ceil((larger - y)/2)
    x_end = (math.floor((larger - x)/2) + x) -1 
    y_end = (math.floor((larger - y)/2) + y) -1

    #attempt to make problem dynamic
    dynamic_array = np.ones([y,x],dtype='float')
    dynamic_array = dynamic_array * -1
    
    #cause I can't get dot or @ to work
    #(also hijack the process to check for
    # eye adjustments)
    for i in range(y_start, y_end):
        for j in range(x_start, x_end):

            #attempt to make this dynamic
            if(dynamic_array[int(crr[i] * (larger/2))][int(crr[j] * (larger/2))] != -1 or dynamic_array[int(crr[j] * (larger/2))][int(crr[i] * (larger/2))] != -1):
                mask[i - y_start][j - x_start] = dynamic_array[int(crr[i] * (larger/2))][int(crr[j] * (larger/2))]
                
            else: 
                mask[i - y_start][j - x_start] = crr[i] * crr[j]
                #hijack attempt
                if (eye > 50):
                    overshot = eye - 50
                    specialValue = overshot / 50 #percent of values in the eye that must be reduced towards 0
                    specialValue = (larger/2)*specialValue
                    specialValue = int(specialValue)
                    mask[i - y_start][j - x_start] = mask[i - y_start][j - x_start] - arr[specialValue-1]
                    if (mask[i - y_start][j - x_start] < 0):
                        mask[i - y_start][j - x_start] = 0 
                    
                    #add to dynamic array
                    dynamic_array[int(crr[i] * (larger/2))][int(crr[j] * (larger/2))] = mask[i - y_start][j - x_start]
                    dynamic_array[int(crr[j] * (larger/2))][int(crr[i] * (larger/2))] = mask[i - y_start][j - x_start]

                elif (eye < 50):
                    overshot = 50 - eye
                    specialValue = overshot / 50 #percent of values in the eye that must be reduced towards 1
                    specialValue = (larger/2)*specialValue
                    specialValue = int(specialValue)
                    mask[i - y_start][j - x_start] = mask[i - y_start][j - x_start] + arr[specialValue-1]
                    if (mask[i - y_start][j - x_start] > 1):
                        mask[i - y_start][j - x_start] = 1 
                    
                    #add to dynamic array
                    dynamic_array[int(crr[i] * (larger/2))][int(crr[j] * (larger/2))] = mask[i - y_start][j - x_start]
                    dynamic_array[int(crr[j] * (larger/2))][int(crr[i] * (larger/2))] = mask[i - y_start][j - x_start]

    #make copy of original image
    modified = np.copy(img)

    #multiply the filter for each layer in the image
    for i in range(3):
        modified[:,:,i] = modified[:,:,i] * mask; 

    return modified