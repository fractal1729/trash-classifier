from helpers import pyramid
from helpers import sliding_window
from featuregrabber import convertToFeatures
import math
import csv
import cv2
import numpy as np
from numpy import genfromtxt
import random
import operator

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
            negCoords.append([y, x, size, 0]);

    return negCoords;

#coords = An array of 4-element arrays of x, y, h, w
def generatePositiveTestCases(coords, w, h, count):
    finalcoords = [];
    for coord in coords:
        top = coord[0]
        left = coord[1]
        height = coord[2]
        width = coord[3]
        size = max(width, height)

        for x in range(0, count):
            additionalsize = random.randint(0, int(size*2))
            ntop = top - random.randint(0, additionalsize)
            nleft = left - random.randint(0, additionalsize)

            if(ntop >=0 and nleft >=0 and ntop+size+additionalsize < h and  nleft+size+additionalsize < w):
                finalcoords.append([int(ntop),int(nleft), int(size+additionalsize), 1])

    return finalcoords

filePrefix = "../../Trash pictures/allpics/"




pictureList = [];


count = 0
with open('trainingdata.csv', 'rb') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
         if count < 1:
            count = count + 1
            print filePrefix + row["1"]
            img = cv2.imread(filePrefix + row["1"] )
            pictureList.append(img)


#unroll pictures and pop them into
coordinates = genfromtxt('trainingdata.csv', delimiter=',')

for i in range(0, len(pictureList)):

    coords = getCoords(coordinates[i + 1])

    img = pictureList[i]
    if img is None or coords is None:
        continue;
    width =  pictureList[i].shape[0]
    height = pictureList[i].shape[1]

    positivetestcases = generatePositiveTestCases(coords, width, height, 30)
    negativetestcases = generateNegativeTestCases(coords,width, height, 50, 200, 100)

    testcases = positivetestcases+negativetestcases



    # for c in negativetestcases:
    #     cropimg = img[c[0]:c[0]+c[2],c[1]:c[1]+c[2]]
    #     cv2.imshow('image',cropimg)
    #     cv2.waitKey(0)
    # # print coords

    #GAUTAM, the below function is what you have made, that should generate all the features
    # convertToFeatures(testcases, img);

    #Once you have called that, then plug it into neural network.py
