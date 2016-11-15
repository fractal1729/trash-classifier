import cv2
import numpy
import argparse
from os import listdir
from os.path import isfile, join

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=False, help="Path to the image")
ap.add_argument("-d", "--folder", required=False, help="Path to the folder")
args = vars(ap.parse_args())

def blurImg(img, blurType):
    # kernel = numpy.ones((5,5),numpy.float32)/25          #kernal filter blur pt1
    # blur = cv2.filter2D(img,-1,kernel)                    #Kernal filter blur pt2
    # blur = cv2.blur(img,(5,5))                           #normal blur
    # blur = cv2.GaussianBlur(img,(5,5),0)                 #gaussian blur
    blur = cv2.medianBlur(img,5)                       #median blur
    # blur = cv2.bilateralFilter(img,9,75,75)              #bilateral filter blur

    return blur

if __name__ == "__main__":
    # image = cv2.imread(args["image"])
    mypath=args["folder"]
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

    if len(onlyfiles) > 0:
        images = numpy.empty(len(onlyfiles), dtype=object)
        for n in range(0, len(onlyfiles)):
          images[n] = cv2.imread( join(mypath,onlyfiles[n]) )
    elif (cv2.imread(args["image"]) != None):
        images = numpy.empty(1, dtype=object)
        images[1] = cv2.imread(args["image"])
    else:
        raise ValueError('Invalid arguments; image or directory path reference needed')


    for img in images:
        blur = blurImg(img)

        vis = numpy.concatenate((img, blur), axis=1)
        cv2.imshow("Orig and Blur", vis)
        cv2.waitKey()

        # clone = img.copy()
        # cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
        # cv2.imshow("Window", clone)




        # plt.subplot(121),plt.imshow(img),plt.title('Original')
        # plt.xticks([]), plt.yticks([])
        # plt.subplot(122),plt.imshow(blur),plt.title('Averaging')
        # plt.xticks([]), plt.yticks([])
        # plt.show()
