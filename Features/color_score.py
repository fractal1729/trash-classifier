import sys
import math
import cv2
import numpy as np
from matplotlib import pyplot as plt

FOLDER_NAME = './../Sample_Images/'
NUM_IMAGES = 22 # max image number

WEIGHT_SAND = 0.8
WEIGHT_SEAWEED = 0.2

sandThresh = 150 # minimum distance from average sand color to be marked as not sand
seaweedThresh = 50 # same for seaweed

def score(img, average):
    height, width, channels = img.shape
    sand = [194, 178, 128];
    seaweed = [55, 65, 42];
    score = 0;
    for i in range(height):
        for j in range(width):
            #px = img[i][j]
            #dist_sand = math.sqrt(math.pow((px[0] - sand[0]),2) + math.pow((px[1] - sand[1]),2) + math.pow((px[2] - sand[2]),2));
            #dist_seaweed = math.sqrt(math.pow((px[0] - seaweed[0]),2) + math.pow((px[1] - seaweed[1]),2) + math.pow((px[2] - seaweed[2]),2))
            #if dist_sand < dist_seaweed:
            #    score = score + (WEIGHT_SAND * math.pow(dist_sand, 2))
            #else:
            #    score = score + (WEIGHT_SEAWEED * math.pow(dist_seaweed, 2))
            dist = math.sqrt(math.pow((px[0] - average[0]),2) + math.pow((px[1] - average[1]),2) + math.pow((px[2] - sand[2]),2));
            score = score +

    return score / (height * width)

def imageAverage(img):
    height, width, channels = img.shape
    sum = [0, 0, 0]
    for i in range(height):
        for j in range(width):
            sum = np.add(sum,img[i][j])

    return sum / (width * height)

for imgnum in range(1, NUM_IMAGES):
    print(FOLDER_NAME+str(imgnum)+'.jpg')
    img = cv2.imread(FOLDER_NAME+str(imgnum)+'.jpg')
    resized_img = cv2.resize(img, (50, 50))
    img_score = score(resized_img, imageAverage(img))
    print(str(imgnum) + ", " + str(img_score))
