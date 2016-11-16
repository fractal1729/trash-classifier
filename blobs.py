# Standard imports
import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys

numimages = 22 # max image number
imgnum = 1 # keeps track of which image we're on
img = cv2.imread('sample_images/'+str(imgnum)+'.jpg', cv2.IMREAD_GRAYSCALE)

def keypress(event):
	if event.key == 'escape': # exit
		plt.close()
		sys.exit()

	global imgnum
	sys.stdout.flush()

	if event.key == 'right' or event.key == 'down': # scroll forward one image
		imgnum = min(imgnum+1, numimages)
	if event.key == 'left' or event.key == 'up': # scroll backward one image
		imgnum = max(imgnum-1, 1)

	img = cv2.imread('sample_images/'+str(imgnum)+'.jpg', cv2.IMREAD_GRAYSCALE)
	plt.imshow(img)
	plt.title('Image '+str(imgnum)+' of '+str(numimages)), plt.xticks([]), plt.yticks([])
	plt.draw()

plt.figure().canvas.mpl_connect('key_press_event', keypress)
imgplot = plt.imshow(img)
plt.title('Image '+str(imgnum)+' of '+str(numimages)), plt.xticks([]), plt.yticks([])
plt.show()


# # Set up the detector with default parameters.
# detector = cv2.SimpleBlobDetector()
 
# # Detect blobs.
# keypoints = detector.detect(img)
 
# # Draw detected blobs as red circles.
# # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
# img_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
