# Standard imports
import cv2
import sys
import numpy as np
from matplotlib import pyplot as plt

numimages = 22 # max image number
imgnum = 1 # keeps track of which image we're on
minThresh = 100 #
maxThresh = 200 #
minArea = 1500

def keypress(event):
	if event.key == 'escape': # exit
		plt.close()
		sys.exit()

	global imgnum, minThresh, maxThresh, minArea
	sys.stdout.flush()

	if event.key == 'right' or event.key == 'down': # scroll forward one image
		imgnum = min(imgnum+1, numimages)
	if event.key == 'left' or event.key == 'up': # scroll backward one image
		imgnum = max(imgnum-1, 1)
	if event.key == 'q': # decrement minimum threshold by 50
		minThresh = minThresh - 50
	if event.key == 'w': # increment minimum threshold by 50
		minThresh = minThresh + 50
	if event.key == 'o': # decrement maximum threshold by 50
		maxThresh = maxThresh - 50
	if event.key == 'p': # increment maximum threshold by 50
		maxThresh = maxThresh + 50
	if event.key == '1': # decrement minimum area by 50
		minArea = minArea - 50
	if event.key == '2': # increment minimum area by 50
		minArea = minArea + 50

	blobDetect(imgnum, minThresh, maxThresh, minArea) # reload image

def blobDetect(imgnum, minThresh, maxThresh, minArea): # min and max thresholds on gradient steepness
	global numimages

	params = cv2.SimpleBlobDetector_Params()

	# Change thresholds
	params.minThreshold = minThresh;
	params.maxThreshold = maxThresh;

	# Filter by Area.
	params.filterByArea = True
	params.minArea = minArea

	img = cv2.imread('sample_images/'+str(imgnum)+'.jpg',cv2.IMREAD_GRAYSCALE)

	detector = cv2.SimpleBlobDetector(params)

	# Detect blobs.
	keypoints = detector.detect(img)

	# Draw detected blobs as red circles.
	# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
	img_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

	imgplot = plt.imshow(img_with_keypoints)
	plt.title('Values: ('+str(minThresh)+','+str(maxThresh)+ ','+str(minArea)+')'), plt.xticks([]), plt.yticks([])
	plt.draw()
	# If you want you can change this directory to sample_images (the ones taken
	# at the beach), but the images in there are so large that edge detection
	# becomes less useful (try it out and see).
	# My gut feeling is that the more compressed the image, the more useful edges are.

plt.figure().canvas.mpl_connect('key_press_event', keypress)
blobDetect(imgnum, minThresh, maxThresh, minArea)
plt.show()
