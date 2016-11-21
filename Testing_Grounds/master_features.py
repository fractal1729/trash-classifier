import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

COLOR_THRESH = 150
EDGE_MIN_THRESH = 100
EDGE_MAX_THRESH = 200

def feature_images(img):
    color = cv2.cvtColor(colorDetect(img, COLOR_THRESH), cv2.COLOR_BGR2GRAY)
    edge = cv2.Canny(img, EDGE_MIN_THRESH, EDGE_MAX_THRESH)
    #edge = cv2.cvtColor(cv2.Canny(img,EDGE_MIN_THRESH,EDGE_MAX_THRESH), cv2.COLOR_BGR2GRAY)
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    return [color, edge, grayscale]

def feature_list(img, coords):
    window_features = [[]]*len(coords)
    feat_imgs = feature_images(img)

    for i in range(len(coords)):
        window_features[i] = [crop(feat_imgs[0],coords[i]).flatten(), crop(feat_imgs[1],coords[i]).flatten(), crop(feat_imgs[2],coords[i]).flatten()]

    return window_features

def features(img):
    color = cv2.cvtColor(colorDetect(img, COLOR_THRESH), cv2.COLOR_BGR2GRAY).flatten()
    edge = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), EDGE_MIN_THRESH, EDGE_MAX_THRESH).flatten()
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).flatten()

    return np.append(color, edge, grayscale)

def crop(img, coords):
    crop_img = img[coords[0]:coords[0]+coords[2], coords[1]:coords[1]+coords[2]]
    return crop_img

def colorDetect(img, thresh):

    height, width, channels = img.shape;
    sand = [194, 178, 128];
    new_image = np.zeros((height,width,channels), np.uint8);

    for i in range(height):
        for j in range(width):
			px = img[i][j]
			dist_sand = math.sqrt(math.pow((px[0] - sand[0]),2) + math.pow((px[1] - sand[1]),2) + math.pow((px[2] - sand[2]),2))
			# dist_seaweed = math.sqrt(math.pow((px[0] - seaweed[0]),2) + math.pow((px[1] - seaweed[1]),2) + math.pow((px[2] - seaweed[2]),2))
			if dist_sand > thresh:
				new_image[i][j] = [255,255,255]

	return new_image

#image1 = cv2.imread('3.jpg', -1)
#coords1 = [[0,0,100,100], [0,0,100,100]]
#feat_imgs_1 = feature_list(image1, coords1)

#cv2.imshow('color', np.squeeze(np.asarray(feat_imgs_1[0])))
#cv2.waitkey(0)
#cv2.imshow('edge', feat_imgs_1[1])
#cv2.waitkey(0)
#cv2.imshow('grayscale', feat_imgs_1[2])
#cv2.waitkey(0)

# image = cv2.imread('./../Sample_Images/3.jpg')
# feature_images(image)
