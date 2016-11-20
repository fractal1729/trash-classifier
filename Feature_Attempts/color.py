import sys
import math
import cv2
import numpy as np
from matplotlib import pyplot as plt

FOLDER_NAME = './../Online Images/'
NUM_IMAGES = 22 # max image number

imgnum = 1 # keeps track of which image we're on
thresh = 150 # minimum distance from average sand color to be marked as not sand

def keypress(event):
	if event.key == 'escape': # exit
		plt.close()
		sys.exit()

	global imgnum, thresh
	sys.stdout.flush()

	if event.key == 'x': # scroll forward one image
		imgnum = min(imgnum+1, NUM_IMAGES)
	if event.key == 'z': # scroll backward one image
		imgnum = max(imgnum-1, 1)
	if event.key == 'q': # decrement threshold by 5
		thresh = thresh - 5
	if event.key == 'w': # increment threshold by 5
		thresh = thresh + 5
	if event.key == '1': # decrement threshold by 10
		thresh = thresh - 10
	if event.key == '2': # increment threshold by 10
		thresh = thresh + 10

	plot(imgnum, thresh) # reload image

def detect(img, thresh):
	height, width, channels = img.shape
	sand = [194, 178, 128]
	new_image = np.zeros((height,width,channels), np.uint8)

	for i in range(height):
		for j in range(width):
			px = img[i][j]
			dist = math.sqrt(math.pow((px[0] - sand[0]),2) + math.pow((px[1] - sand[1]),2) + math.pow((px[2] - sand[2]),2))
			if dist > thresh:
				new_image[i][j] = [255,255,255]

	return new_image

def plot(imgnum, thresh): # threshold on gradient steepness
	global NUM_IMAGES

	img = cv2.imread(FOLDER_NAME+str(imgnum)+'.jpg')

	result = detect(img, thresh)

	plt.subplot(121),plt.imshow(img,cmap = 'gray')
	plt.title('Original Image ('+str(imgnum)+' of '+str(NUM_IMAGES)+')'), plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow(result,cmap = 'gray')
	plt.title('New Image ('+str(thresh)+')'), plt.xticks([]), plt.yticks([])

	plt.draw()

plt.figure().canvas.mpl_connect('key_press_event', keypress)
plot(imgnum, thresh)
plt.show()
