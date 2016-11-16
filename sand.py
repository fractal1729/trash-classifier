import cv2
import numpy as np
import matplotlib.pyplot as plt
from helpers import sliding_window
import scipy.stats as stats

# get average color of sand
sandimg = cv2.imread('./../sample_images/sand.jpg',0)

h = sorted(np.squeeze(np.asarray(sandimg)))

fit = stats.norm.pdf(h, np.mean(h), np.std(h))  #this is a fitting indeed

plt.plot(h,fit,'-o')

plt.hist(h,normed=True)      #use this to draw histogram of your data

plt.show()                   #use may also need add this 

# average_color = np.average(np.average(img,axis=0),axis=0) # get average color

# img = cv2.imread('./../sample_images/1.jpg')
# win_size = 32
# windows = sliding_windows(img, win_size, (win_size, win_size))
# for (col, row, window) in windows:
# 	if window.shape[0] != win_size or window.shape[1] != win_size:
# 		continue
# 	window_average_color = np.average(np.average(window,axis=0),axis=0)