from helpers import pyramid
from helpers import sliding_window
import math
import csv
import cv2
import numpy as np
from numpy import genfromtxt
import random

def getCoords(row):
    index = 1
    coords = []
    while (index < len(row)) and (not math.isnan(row[index])) :
        coords.append([row[index],row[index+1],row[index+2],row[index+3]])
        index = index + 4
    return coords

def generateNegativeTestCases(img, coords, size):
    negCoords = [];
    width = len(img[0])
    height = len(img)
    for x in range(0, width - size):
        for y in range(0, height - size):
            for coord in coords:
                if (x < (coord[0] + coords[4])) && ((x + width) > coord[0]) && (y < (coord[1] + coord[3])) && ((y + height) > coord[1]):
                    continue
                else:
                    negCoords.append(coord)
    return negCoords                


#coords = An array of 4-element arrays of x, y, h, w
def generatePositiveTestCases(coords, count):
    finalcoords = [];
    for coord in coords:
        top = coord[0]
        left = coord[1]
        height = coord[2]
        width = coord[3]
        size = max(width, height)

        for x in range(0, count):
            additionalsize = random.randint(0, int(size/2))
            top = top - random.randint(0, additionalsize)
            left = left - random.randint(0, additionalsize)
            finalcoords.append([top,left, size+additionalsize])



filePrefix = "../Trash pictures/allpics/"




pictureList = [];


count = 0
with open('trainingdata.csv', 'rb') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
         if count < 10:
             count = count + 1
             img = cv2.imread(filePrefix + row["1"] )
             pictureList.append([img])
             print 1

#unroll pictures and pop them into
coordinates = genfromtxt('trainingdata.csv', delimiter=',')

for i in range(0, len(pictureList)):
    coords = getCoords(coordinates[i + 1])
    positivetestcases = generatePositiveTestCases(coords, 30)
    #negativetestcases =


    print coords
