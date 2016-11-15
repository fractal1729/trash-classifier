#import the necessary packages

import argparse
from Tkinter import *

import cv2
from opencv import imutils

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="Path to the image to be scanned")
args = vars(ap.parse_args())

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread(args["image"])
ratio = image.shape[0] / 500
orig = image.copy
image = imutils.resize(image, height=500)

# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # grayscale rgb
gray = cv2.GaussianBlur(gray, (5, 5), 0)  # blurs image
edged = cv2.Canny(gray, 75, 100)  # finds edges of min dimensions 75,100

# show the original image and the edge detected image
print "STEP 1: Edge Detection"
# cv2.imshow("Image", image)
# cv2.imshow("Edged", edged)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

# loop over the contours
for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.02 * peri, True)

    # cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
    # cv2.imshow(str(peri), image)

    # if our approximated contour has four points, then we
    # can assume that we have found our screen
    if len(approx) == 4:
        screenCnt = approx
        break


# show the contour (outline) of the piece of paper
# print "STEP 2: Find contours of paper"
# cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
# cv2.imshow("Outline", image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()



#########################################################

lowert = 0.0
uppert = 0.0
gausrad = 1

def draw():
    global  lowert
    global  uppert
    global  gausrad

    cv2.destroyAllWindows()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # grayscale rgb
    gray = cv2.GaussianBlur(gray, (gausrad, gausrad), 0)  # blurs image
    edged = cv2.Canny(gray, lowert, uppert)  # finds edges of min dimensions 75,100
    cv2.imshow(str(uppert), edged)
    cv2.imshow("gray", gray)
    cv2.moveWindow("gray", 1000, 0)


def updatelow(val):
    global lowert
    lowert = float(val)
    draw()

def updateupper(val):
    global uppert
    uppert =float(val)
    draw()

def updateBlur(var):
    global gausrad
    if (int(var) % 2 == 1):
        gausrad = max(1,int(var))
        draw()

root = Tk()
var = DoubleVar()
var2 = DoubleVar()
var3 = DoubleVar()

scale = Scale( root, variable = var , command=updatelow,to_=200)
scale.pack(side=LEFT)

scale2 = Scale( root, variable = var2 , command=updateupper,to_=300)
scale2.pack(side=RIGHT)

scale3 = Scale( root, variable = var3 , command=updateBlur, orient=HORIZONTAL,from_=1,to_=99)
scale3.pack(side=BOTTOM)

root.mainloop()















