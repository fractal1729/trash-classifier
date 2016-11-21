import imutils
import cv2
import numpy as np
import math
import random

# FAQ
# Q. What is "yield"?
# A. http://stackoverflow.com/questions/231767/what-does-the-yield-keyword-do


COLOR_THRESH = 150
EDGE_MIN_THRESH = 100
EDGE_MAX_THRESH = 200
TEST_CASE_SIZE = 50

def featuresForImage(img):
    color = cv2.cvtColor(colorDetect(img, COLOR_THRESH), cv2.COLOR_BGR2GRAY)
    edge = cv2.Canny(img, EDGE_MIN_THRESH, EDGE_MAX_THRESH)
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return [color, edge, grayscale]

def extractFeatures(img, coords):
    window_features = [[]]*len(coords)
    feat_imgs = featuresForImage(img)

    for i in range(len(coords)):
        window_features[i] = np.array([cropAndResize(feat_imgs[0],coords[i]).flatten(), cropAndResize(feat_imgs[1],coords[i]).flatten(), cropAndResize(feat_imgs[2],coords[i]).flatten()]).flatten()

    return window_features
#Coords: (y, x, size, 1/0)
def cropAndResize(img, coords):
    # print("Coords: ", coords)
    # print("Image Size: ", len(img), ", ", len(img[0]))
    crop_img = img[coords[0]:coords[0]+coords[2], coords[1]:coords[1]+coords[2]]
    # cv2.imshow(crop_img)
    resizedImg = np.array([])
    # print "Trying to resize Image of size (h, w): (", len(crop_img) , ", ", len(crop_img[0]), ")"
    resizedImg = cv2.resize(crop_img, (TEST_CASE_SIZE, TEST_CASE_SIZE))
    return resizedImg

def colorDetect(img, thresh):

    height, width, channels = img.shape
    sand = [194, 178, 128]
    new_image = np.zeros((height,width,channels), np.uint8)

    for i in range(height):
        for j in range(width):
			px = img[i][j]
			dist_sand = math.sqrt(math.pow((px[0] - sand[0]),2) + math.pow((px[1] - sand[1]),2) + math.pow((px[2] - sand[2]),2))
			# dist_seaweed = math.sqrt(math.pow((px[0] - seaweed[0]),2) + math.pow((px[1] - seaweed[1]),2) + math.pow((px[2] - seaweed[2]),2))
			if dist_sand > thresh:
				new_image[i][j] = [255,255,255]

	return new_image

def getCoords(row):
    index = 1
    coords = []
    while (index < len(row)) and (not math.isnan(row[index])) :
        coords.append([row[index],row[index+1],row[index+2],row[index+3]])
        index = index + 4
    return coords

def generateNegativeTestCases(coords, width, height, minSize, maxSize, count):
    negCoords = [];
    for i in range(0, count):
        size = random.randint(minSize, maxSize)
        y = random.randint(0,height-1-size)
        x = random.randint(0,width-1-size)
        #confirm that this does not overlap of the coordinates
        foundoverlap = False
        for coord in coords:
            if x < coord[1] + coord[3] and x + size > coord[1] and y < coord[0] + coord[2] and y + size  > coord[0]:
                foundoverlap = True
        if not foundoverlap:
            negCoords.append([x, y, size, 0])

    return negCoords

#coords = An array of 4-element arrays of y, x, h, w

# def generatePositiveTestCases(coords, w, h, count):
#     finalcoords = [];
#     for coord in coords:
#         top = coord[0]
#         left = coord[1]
#         height = coord[2]
#         width = coord[3]
#         size = max(width, height)

# def generatePositiveTestCases(coords, w, h, count):
#     finalcoords = [];
#     for coord in coords:
#         top = coord[0]
#         left = coord[1]
#         height = coord[2]
#         width = coord[3]
#         size = max(width, height)

#         for x in range(0, count):
#             additionalsize = random.randint(0, int(size))-size/2
#             ntop = top - random.randint(min(0, additionalsize), max(0, additionalsize))
#             nleft = left - random.randint(min(0, additionalsize), max(0, additionalsize))

#             if(ntop >=0 and nleft >=0 and ntop+size+additionalsize < h and  nleft+size+additionalsize < w):
#                 finalcoords.append([int(ntop),int(nleft), int(size+additionalsize), 1])

#     return finalcoords

def generatePositiveTestCases(coords, width, height, minSize, maxSize, count):
    posCoords = []
    for coord in coords:
        y0 = coord[0]
        x0 = coord[1]
        h = coord[2]
        w = coord[3]

        for k in range(count):
            size = random.randint(minSize, maxSize)
            x = random.randint(0, w)+max(0,x0-size/2)
            y = random.randint(0, h)+max(0,y0-size/2)
            posCoords.append([y,x,size,1])
    return posCoords

def pyramid(image, scale=1.5, minSize=(30,30)):
    """
    Create a succesive list of increasing smaller images aka a pyramid

    :param image: Valid image
    :param scale: Decrease scale factor (float). Larger scale = more decreasing (reaches minSize quicker)
    :param minSize: Minimum image size
    """
    yield image                                                        #initial image is original

    while True:
        yield image
        w = int(image.shape[1] / scale)                                #recursively scale the width down 2/3 (divided 150%)
        image = imutils.resize(image, width=w)                         #return a aspect-ratio maintained scaled image

        if image.shape[0] < minSize[1] or image.shape[1] < minSize[0]: #check for minimum scale, if yes don't return new image
            break

        yield image                                                    #create list of recursively scaled images aka the pyramid


def sliding_window(image, stepSize, windowSize):
        """
        Generate slices of image using windows that slide and resize

        :param image: Source Image
        :param stepSize: How many pixels to skip per slide
        :param windowSize: Size of image window
        """

        for row in xrange(0, image.shape[0], stepSize):
            for col in xrange(0, image.shape[1], stepSize):
                yield (col, row, image[row:row + windowSize[1],col:col + windowSize[0]])

def compressJPG(img, factor):
    """
    Compress a JPG image

    :param img: Source Image
    :param factor: Compression factor; ranges from 0 to 1 if you're trying to make the image smaller
    """
    resizedImg = np.array([])
    resizedImg = cv2.resize(img, (0,0), resizedImg, factor, factor, cv2.INTER_NEAREST)
    return resizedImg
