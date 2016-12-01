import sys
import math
import cv2
import numpy as np
from matplotlib import pyplot as plt

FOLDER_NAME = './../Online_Images/'
NUM_IMAGES = 22 # max image number

imgnum = 1 # keeps track of which image we're on
sandThresh = 150 # minimum distance from average sand color to be marked as not sand
seaweedThresh = 50 # same for seaweed

def keypress(event):
	if event.key == 'escape': # exit
		plt.close()
		sys.exit()

	global imgnum, sandThresh, seaweedThresh
	sys.stdout.flush()

	if event.key == 'x': # scroll forward one image
		imgnum = min(imgnum+1, NUM_IMAGES)
	if event.key == 'z': # scroll backward one image
		imgnum = max(imgnum-1, 1)
	if event.key == 'q': # decrement sandThreshold by 5
		sandThresh = sandThresh - 5
	if event.key == 'w': # increment sandThreshold by 5
		sandThresh = sandThresh + 5
	if event.key == '1': # decrement sandThreshold by 10
		sandThresh = sandThresh - 10
	if event.key == '2': # increment sandThreshold by 10
		sandThresh = sandThresh + 10

	if event.key == 'e': # decrement sandThreshold by 5
		seaweedThresh = seaweedThresh - 5
	if event.key == 'r': # increment sandThreshold by 5
		seaweedThresh = seaweedThresh + 5
	if event.key == '3': # decrement sandThreshold by 10
		seaweedThresh = seaweedThresh - 10
	if event.key == '4': # increment sandThreshold by 10
		seaweedThresh = seaweedThresh + 10

	plot(imgnum, sandThresh, seaweedThresh) # reload image

def detect(img, sandThresh, seaweedThresh):
	height, width, channels = img.shape
	sand = [194, 178, 128]
	seaweed = [55, 65, 42]
	new_image = np.zeros((height,width,channels), np.uint8)

	for i in range(height):
		for j in range(width):
			px = img[i][j]
			dist_sand = math.sqrt(math.pow((px[0] - sand[0]),2) + math.pow((px[1] - sand[1]),2) + math.pow((px[2] - sand[2]),2))
			dist_seaweed = math.sqrt(math.pow((px[0] - seaweed[0]),2) + math.pow((px[1] - seaweed[1]),2) + math.pow((px[2] - seaweed[2]),2))
			if dist_sand > sandThresh and dist_seaweed > seaweedThresh:
				new_image[i][j] = [255,255,255]

	return new_image

def plot(imgnum, sandThresh, seaweedThresh): # sandThreshold on gradient steepness
	global NUM_IMAGES

	img = cv2.imread(FOLDER_NAME+str(imgnum)+'.jpg')

	result = detect(img, sandThresh, seaweedThresh)

	plt.subplot(121),plt.imshow(img,cmap = 'gray')
	plt.title('Original Image ('+str(imgnum)+' of '+str(NUM_IMAGES)+')'), plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow(result,cmap = 'gray')
	plt.title('New Image ('+str(sandThresh)+')'), plt.xticks([]), plt.yticks([])

	plt.draw()

plt.figure().canvas.mpl_connect('key_press_event', keypress)
plot(imgnum, sandThresh, seaweedThresh)
plt.show()
