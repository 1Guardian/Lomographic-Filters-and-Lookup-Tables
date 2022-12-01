#==============================================================================
#
# Class : CS 5420
#
# Author : Tyler Martin
#
# Project Name : Project 5 | Lomographic Filters
#
# Date: 11-8-2022
#
# Description: This project implements a simple GUI to apply and control
#              a LUT filter on the red channel of an input image as well 
#              as controlling a vignette filter that is created via use of
#              simple matrix multiplication to make a filter and then
#              overarching channel multiplication to apply the filter to the 
#              image. Pressing 'S' saves the file to <filename>.<img extension> while 
#              pressing 'Q' quits the program. After sliders are adjusted, press 
#              the "Apply" button just below them in the GUI to apply the effects
#              to the image. (This was done because of how python GUI Sliders update 
#              after every tick, thus making the GUI incredibly laggy as it tries to
#              do multiple applications per tick of each bar)
#
# Notes: Since I know you prefer to read and work in C++, this file is set
#        up to mimic a standard C/C++ flow style, including a __main__()
#        declaration for ease of viewing. Also, while semi-colons are not 
#        required in python, they can be placed at the end of lines anyway, 
#        usually to denote a specific thing. In my case, they denote globals, 
#        and global access, just to once again make it easier to parse my code
#        and see what it is doing and accessing.
#
#==============================================================================

#"header" file imports
from imports import *
from checkImages import *
from getMetaData import *
from saveImage import *
from ApplyLUT import *
from vignetteMask import *
from resizeImage import *
from haloVignette import *
from squareVignetteMask import *

#================================================================
#
# GLOBALS
#
#================================================================
currentImg = 0;
maxSize = 0;
currentImage = 0;
originalName = "out";
originalImage = 0;
x = 1080;
y = 720;
globalpath = "/"
fixed = FALSE

#================================================================
#
# Class: ImageBox
#
# Description: This class serves as the GUI for the application.
#              It opens displaying the first image in the directory
#              and can cycle between other images present in the 
#              directory. It also displays metadata associated with
#              the image being displayed. It is included here along
#              with main, because while python can import other files
#              and functions similar to headers, for functions to be
#              imported, it requires mass re-importing to make sure 
#              the class has the access it needs, which slows the 
#              program down and causes tight coupling. 
#
#================================================================
class imageBox(Tk):
    def __init__(self):
        super().__init__()
        
        #gain temporary access to globals
        global currentImage;
        global originalImage;
        global x;
        global y;

        #setup the basic window features
        self.title('Lomo Window')
        self.resizable(0, 0)

        #no windows smaller than 720x1080
        #(Also setting a variable to let me know
        # how long the word wrap should be)
        if (x < 1080 or y < 720):
            self.geometry("1080x720")
            self.realWindowLength = 1080
        else:
            self.geometry(str(x) + 'x' + str(int(y + (y/2))))
            self.realWindowLength = x
    
        #making an imageBox frame
        self.imgBox = Frame(self, relief=RIDGE, borderwidth=5)
        self.imgBox.pack(side=TOP)

        #convert our image back to PIL format
        #(essentially just swapping bgr pixel
        # order to rgb for pil)
        self.blue, self.green, self.red = cv2.split(resizeImage(originalImage, x, y, getMetaData(originalImage)))[0:3]
        self.img = cv2.merge((self.red, self.green, self.blue))
        self.icon = ImageTk.PhotoImage(image=Image.fromarray(self.img))

        #anchoring the image to the widget
        #(I have no idea what this does, but
        #from what I have read, the C side of 
        #python requires that Tkinter image
        #references have an 'anchor' point
        #which is literally just a pointer
        #on the C side, so we just force it to
        #make one by making a hard reference)
        self.icon_size = Label(self.imgBox)
        self.icon_size.image = self.icon
        self.icon_size.configure(image=self.icon)
        self.icon_size.pack(side=LEFT)

        #testing label
        label = Label(self)
        label.pack()

        #slider position variables
        vignetteVar = DoubleVar()
        squarevignetteVar = DoubleVar()
        halovignetteVar = DoubleVar()
        redlutVar = DoubleVar()
        greenlutVar = DoubleVar()
        bluelutVar = DoubleVar()
        rootRef = self

        #making an apply button and labels
        self.applyButton = Button(self, text="Apply", command=lambda: rootRef.applyFilter(rootRef))
        self.applyButton.pack(side=BOTTOM)  

        #making a slider for the vignette
        vignetteLabel = Label(self, text="True Vignette Slider")
        vignetteLabel.pack(side=BOTTOM)
        self.vignetteSlider = Scale(self, from_=-1, to=100, variable=vignetteVar, orient=HORIZONTAL)
        self.vignetteSlider.pack(fill="x", side=BOTTOM)  

        #making a slider for the 'halo' vignette version
        halovignetteLabel = Label(self, text="Halo Vignette Slider")
        halovignetteLabel.pack(side=BOTTOM)
        self.halovignetteSlider = Scale(self, from_=-1, to=100, variable=halovignetteVar, orient=HORIZONTAL)
        self.halovignetteSlider.pack(fill="x", side=BOTTOM)  

        #making a slider for the 'halo' vignette version
        squarevignetteLabel = Label(self, text="Square Vignette Slider")
        squarevignetteLabel.pack(side=BOTTOM)
        self.squarevignetteSlider = Scale(self, from_=-1, to=100, variable=squarevignetteVar, orient=HORIZONTAL)
        self.squarevignetteSlider.pack(fill="x", side=BOTTOM)  

        #making a slider for the Red Channel LUT
        redlutLabel = Label(self, text="Red LUT Slider")
        redlutLabel.pack(side=BOTTOM)
        self.redlutSlider = Scale(self, from_=-1, to=100, variable=redlutVar, orient=HORIZONTAL)
        self.redlutSlider.pack(fill="x", side=BOTTOM)

        #making a slider for the Green Channel LUT
        greenlutLabel = Label(self, text="Green LUT Slider")
        greenlutLabel.pack(side=BOTTOM)
        self.greenlutSlider = Scale(self, from_=-1, to=100, variable=bluelutVar, orient=HORIZONTAL)
        self.greenlutSlider.pack(fill="x", side=BOTTOM)

        #making a slider for the Blue Channel LUT
        bluelutLabel = Label(self, text="Blue LUT Slider")
        bluelutLabel.pack(side=BOTTOM)
        self.bluelutSlider = Scale(self, from_=-1, to=100, variable=greenlutVar, orient=HORIZONTAL)
        self.bluelutSlider.pack(fill="x", side=BOTTOM)

        #set each slider to -1, aka, inactive
        self.redlutSlider.set(-1)
        self.greenlutSlider.set(-1)
        self.bluelutSlider.set(-1)
        self.vignetteSlider.set(-1)
        self.halovignetteSlider.set(-1)
        self.squarevignetteSlider.set(-1)

        #set key handler listener
        self.bind("<Key>", self.key_handler)

        #listner to keep window open and updating
        self.imgBox.after(1000, self.update)

    #===========================================
    #this is a callback function. It is fired
    #when a bind event happens to check for a key
    #fire event. If a valid key fire is detected,
    #globals are updated, and the displayed image
    #is as well
    #===========================================
    def key_handler(self, event):
        #gain access to the global
        global currentImg;
        global maxSize;
        global ImgList;
        global ImagePathList;
        global x;
        global y;
        action = event.keysym;

        #listen for keystrokes
        if action == 'q':
            quit();
        
        if action == 's':
            saveImage(currentImage, pathlib.Path(globalpath).suffix, "./", originalName)

    #===========================================
    #this is a callback function fired from the
    #update button. It will run the lut application
    #as well as the image vignette application
    #and then update the image displayed
    #===========================================
    def applyFilter(self, a):

        #global access
        global originalImage;
        global currentImage;
        global fixed;
        newimage = np.copy(originalImage)

        #apply lut on red channel
        if(self.redlutSlider.get() != -1):
            newimage = applyRedLut(newimage, 0.20-((self.redlutSlider.get()/100)*(0.20-0.08)))

        #apply lut on green channel
        if(self.greenlutSlider.get() != -1):
            newimage = applyGreenLut(newimage, 0.20-((self.greenlutSlider.get()/100)*(0.20-0.08)))

        #apply lut on red channel
        if(self.bluelutSlider.get() != -1):
            newimage = applyBlueLut(newimage, 0.20-((self.bluelutSlider.get()/100)*(0.20-0.08)))

        #apply the vignette effect on the previously modified image
        if(self.vignetteSlider.get() != -1):
            newimage = changeVinnete(newimage, (100-self.vignetteSlider.get()))

        #apply the vignette effect on the previously modified image
        if(self.halovignetteSlider.get() != -1):
            newimage = haloVignette(newimage, (self.halovignetteSlider.get()), fixed)

        #apply the vignette effect on the previously modified image
        if(self.squarevignetteSlider.get() != -1):
            newimage = squareVignette(newimage, (100-self.squarevignetteSlider.get()))

        #update the image
        currentImage = newimage
        self.blue, self.green, self.red = cv2.split(resizeImage(newimage, x, y, getMetaData(newimage)))[0:3]
        self.img = cv2.merge((self.red, self.green, self.blue))
        self.icon = ImageTk.PhotoImage(image=Image.fromarray(self.img))

        #same reference 'achor' stuff, but now we update
        #the image instead of making a new one
        self.icon_size.image = self.icon
        self.icon_size.configure(image=self.icon)

        return newimage


    #===========================================
    #this is a callback function. It is fired
    #every 100 milliseconds to check for a key
    #fire event. If a key fire is detected, the
    #globals are updated, and the displayed image
    #is as well
    #===========================================
    def update(self):
        
        #recursive call to keep listening
        self.imgBox.after(100, self.update)

#================================================================
#
# Function: __main__
#
# Description: This function is the python equivalent to a main
#              function in C/C++ (added just for ease of your
#              reading, it has no practical purpose)
#
#================================================================

def __main__(argv):

    #gain access to our globals
    global maxSize;
    global currentImg;
    global currentImage;
    global originalImage;
    global originalName;
    global x;
    global y;
    global globalpath;
    global fixed;

    #variable to hold path
    path = "nothing"

    # get arguments and parse
    try:
      opts, args = getopt.getopt(argv,"fh:i:")
    except getopt.GetoptError:
        print("lomo.py -h -i imagefile")
        print("===========================================================================================================")
        print("-i : image file that you want to work on")
        sys.exit(2)
    for opt, arg in opts:
        if opt == ("-h"):
            print("lomo.py -h -i imagefile")
            print("===========================================================================================================")
            print("-i : image file that you want to work on")
            sys.exit(2)
        elif opt in ("-i", "--img"):
            path = arg
        elif opt in ("-f", "--fixed"):
            fixed = True

    #make sure we got at the least, a path
    if (path == "nothing"):
        print("you must provide an image to start with!")
        sys.exit(2)

    #set max size global
    originalImage = checkImages(path)
    currentImage = originalImage
    globalpath = path
    originalName = os.path.splitext(os.path.basename(path))[0]

    #make the imagebrowser gui
    ws = imageBox()
    ws.mainloop()

#start main
argv = ""
__main__(sys.argv[1:])