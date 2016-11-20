import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
from Neural_Network.master_features import features

NUM_IMAGES = 22 # max image number
FOLDER_NAME = './Online_Images/'
MAX_WINDOW_SIZE = 200
MIN_WINDOW_SIZE = 20

imgnum = 1 # keeps track of which image we're on
img = cv2.imread(FOLDER_NAME+str(imgnum)+'.jpg')
imgH,imgW,channels = img.shape

win_size = 50 # default size of sliding windows

def onclick(event):
    ix, iy = event.xdata, event.ydata
    if ix and iy:
    	ix = int(ix)
    	iy = int(iy)
    	print 'x = %d, y = %d'%(ix, iy)
    	winL = (win_size)*(ix/win_size) # left column coordinate
    	winT = (win_size)*(iy/win_size) # top row coordinate
    	winR = min(winL+win_size, imgW) # right column coordinate
    	winB = min(winT+win_size, imgH) # bottom row coordinate
    	window = img[winT:winB,winL:winR]
    	
    	plot_window(window)

    	plt.show()

def plot_window(window):
	fig2 = plt.figure()
	color, edge, grayscale = features(window)
	plt.subplot(121),plt.imshow(window)
	plt.title('Window'), plt.xticks([]), plt.yticks([])
	plt.subplot(122),plt.imshow(grayscale)
	plt.title('Grayscale'), plt.xticks([]), plt.yticks([])
	plt.subplot(221),plt.imshow(edge)
	plt.title('Edges'), plt.xticks([]), plt.yticks([])
	plt.subplot(222),plt.imshow(color)
	plt.title('Colors'), plt.xticks([]), plt.yticks([])

def keypress(event):
	if event.key == 'escape': # exit
		plt.close()
		sys.exit()

	global imgnum, win_size, img, imgH, imgW
	sys.stdout.flush()

	if event.key == 'x': # scroll forward one image
		imgnum = min(imgnum+1, NUM_IMAGES)
	if event.key == 'z': # scroll backward one image
		imgnum = max(imgnum-1, 1)

	if event.key == 'v': # increment window size
		win_size = min(win_size+10,MAX_WINDOW_SIZE)
	if event.key == 'c': # decrement window size
		win_size = max(win_size-10,MIN_WINDOW_SIZE)

	img = cv2.imread(FOLDER_NAME+str(imgnum)+'.jpg')
	imgH,imgW,channels = img.shape
	img_with_windows = draw_windows(win_size, win_size, img)
	plt.imshow(img_with_windows)
	plt.title('Image '+str(imgnum)+' of '+str(NUM_IMAGES)), plt.xticks([]), plt.yticks([])
	plt.draw()

def draw_windows(winW, winH, img):
	imgCopy = np.copy(img)
	imgH,imgW,channels = img.shape
	for i in range(-1*((-1*imgH)/winH)): # -1*((-1*imgH)/winH) is the ceiling of imgH/winH
		imgCopy[winH*i,:] = [[0,0,0]]*imgW
	for i in range(-1*((-1*imgW)/winW)): # -1*((-1*imgW)/winW) is the ceiling of imgW/winW
		imgCopy[:,winW*i] = [[0,0,0]]*imgH
	return imgCopy

fig = plt.figure()
fig.canvas.mpl_connect('key_press_event', keypress)
fig.canvas.mpl_connect('button_press_event', onclick)

img_with_windows = draw_windows(win_size, win_size, img)
plt.imshow(img_with_windows)
plt.title('Image '+str(imgnum)+' of '+str(NUM_IMAGES)), plt.xticks([]), plt.yticks([])
plt.show()