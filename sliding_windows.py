# import the necessary packages
from helpers import pyramid
from helpers import sliding_window
import argparse
import time
import cv2
from os import listdir
from os.path import isfile, join
import numpy

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False, help="Path to the image")
ap.add_argument("-d", "--folder", required=False, help="Path to the folder")
args = vars(ap.parse_args())

# image = cv2.imread(args["image"])

mypath=args["folder"]
onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
images = numpy.empty(len(onlyfiles), dtype=object)
for n in range(0, len(onlyfiles)):
  images[n] = cv2.imread( join(mypath,onlyfiles[n]) )

for image in images:
    win_size = 16;
    (winW, winH) = (win_size, win_size)

    for resized in pyramid(image, scale=1.5, minSize=(20,20)):
        for (x, y, window) in sliding_window(resized, stepSize=win_size, windowSize=(winW, winH)):
            # if the window does not meet our desired window size, ignore it
            if window.shape[0] != winH or window.shape[1] != winW:
                continue

            #CLASSIFY SHIT HERE

            # since we do not have a classifier... ahem... we'll just draw the window
            clone = resized.copy()
            cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
            cv2.imshow("Window", clone)
            cv2.waitKey(1)
            # time.sleep(0.0001)
