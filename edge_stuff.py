import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt

numimages = 26 # max image number
imgnum = 1 # keeps track of which image we're on
minThresh = 100 #
maxThresh = 200 #

def keypress(event):
	if event.key == 'escape': # exit
		plt.close()
		sys.exit()

	global imgnum, minThresh, maxThresh
	sys.stdout.flush()

	if event.key == 'right' or event.key == 'down': # scroll forward one image
		imgnum = min(imgnum+1, numimages)
	if event.key == 'left' or event.key == 'up': # scroll backward one image
		imgnum = max(imgnum-1, 1)
	if event.key == 'q': # decrement minimum edge threshold by 10
		minThresh = minThresh - 10
	if event.key == 'w': # increment minimum edge threshold by 10
		minThresh = minThresh + 10
	if event.key == 'o': # decrement maximum edge threshold by 10
		maxThresh = maxThresh - 10
	if event.key == 'p': # increment maximum edge threshold by 10
		maxThresh = maxThresh + 10
	if event.key == '1': # decrement minimum edge threshold by 50
		minThresh = minThresh - 50
	if event.key == '2': # increment minimum edge threshold by 50
		minThresh = minThresh + 50
	if event.key == '9': # decrement maximum edge threshold by 50
		maxThresh = maxThresh - 50
	if event.key == '0': # increment maximum edge threshold by 50
		maxThresh = maxThresh + 50

	edgeDetect(imgnum, minThresh, maxThresh) # reload image

def edgeDetect(imgnum, minThresh, maxThresh): # min and max thresholds on gradient steepness
	global numimages
	
	img = cv2.imread('windows/Online/'+str(imgnum)+'.jpg',0)
	# If you want you can change this directory to sample_images (the ones taken
	# at the beach), but the images in there are so large that edge detection
	# becomes less useful (try it out and see).
	# My gut feeling is that the more compressed the image, the more useful edges are.

	edges = cv2.Canny(img,minThresh,maxThresh)

	plt.subplot(121),plt.imshow(img,cmap = 'gray')
	plt.title('Original Image ('+str(imgnum)+' of '+str(numimages)+')'), plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow(edges,cmap = 'gray')
	plt.title('Edge Image ('+str(minThresh)+','+str(maxThresh)+')'), plt.xticks([]), plt.yticks([])

	plt.draw()

plt.figure().canvas.mpl_connect('key_press_event', keypress)
edgeDetect(imgnum, minThresh, maxThresh)
plt.show()