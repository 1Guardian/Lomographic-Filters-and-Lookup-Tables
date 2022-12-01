# Lomographic-Filters-and-Lookup-Tables
This program extends the functionality of the tkinter image browser and adds sliders to apply various modifications to the supplied image

## Notes
This project implements an extended version of my tkinter UI to allow modification of an image. The first set of sliders allows the user to shift the red blue and green channels individually. The second set of sliders allows the user to apply a vignette mask to the image. The first vignette type is a "dumb" vignette, and just darkens the image around a centered circle in the middle of the image, then blurs the image with an rxr kernel, where r is defined as the radius. The vignette mask is a "true" vignette where the image darkens more as you get further away from the center of the image. The third is a "boxcar" vignette, which is a modified boxcar kernel, which generates a vignette in the shape of a diamond, that becomes more square the higher the intensity of the mask is. 

## Usage:
<pre>
ptyhon lomo.py -h-i imagefile
