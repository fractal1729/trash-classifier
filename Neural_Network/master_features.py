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
    edge = cv2.Canny(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), EDGE_MIN_THRESH, EDGE_MAX_THRESH)
    #edge = cv2.cvtColor(cv2.Canny(img,EDGE_MIN_THRESH,EDGE_MAX_THRESH), cv2.COLOR_BGR2GRAY)
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return [color, edge, grayscale]

def main(img, coords):
    window_features = np.empty(len(coords))

    for i in range(len(coords)):
        crop_img = crop(img, coords[i])
        window_features[i] = features(crop_img)

    return window_features

def features(img):
    color = cv2.cvtColor(colorDetect(img, COLOR_THRESH), cv2.COLOR_BGR2GRAY).flatten()
    edge = cv2.cvtColor(cv2.Canny(img,EDGE_MIN_THRESH,EDGE_MAX_THRESH), cv2.COLOR_BGR2GRAY).flatten()
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).flatten()

    return np.append(color, edge, grayscale)

def crop(img, coords):
    crop_img = img[coords[1]:coords[2], coords[0]:coords[2]]
    return crop_img

def colorDetect(img, thresh):
	height, width, channels = img.shape
	sand = [194, 178, 128]
	# seaweed = [55, 65, 42]
	new_image = np.zeros((height,width,channels), np.uint8)

	for i in range(height):
		for j in range(width):
			px = img[i][j]
			dist_sand = math.sqrt(math.pow((px[0] - sand[0]),2) + math.pow((px[1] - sand[1]),2) + math.pow((px[2] - sand[2]),2))
			# dist_seaweed = math.sqrt(math.pow((px[0] - seaweed[0]),2) + math.pow((px[1] - seaweed[1]),2) + math.pow((px[2] - seaweed[2]),2))
			if dist_sand > thresh:
				new_image[i][j] = [255,255,255]

	return new_image


# image = cv2.imread('./../Sample_Images/3.jpg')
# feature_images(image)