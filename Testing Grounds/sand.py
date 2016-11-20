import cv2
import numpy as np
import matplotlib.pyplot as plt
from helpers import sliding_window
import scipy.stats as stats

# get average color of sand
sandimg = cv2.imread('./sample_images/1.jpg',0)

sandpix = np.array(sorted(np.matrix(sandimg).getA1())) # unrolls the matrix into an array, and sorts it

dist = getattr(stats, 'gamma')
print('hi')
param = dist.fit(sandpix)
print('hi2')
fit = dist.pdf(*param[:-2], loc=param[-2], scale=param[-1], normed=True)
print('hi3')

# fit = stats.beta.pdf(sandpix, np.mean(sandpix), np.std(sandpix))

plt.plot(fit)

binwidth = 3
hist = plt.hist(sandpix, normed=True, bins=range(min(sandpix), max(sandpix) + binwidth, binwidth))

plt.show()

# checked = [False]*256
# sumsquares = 0

# bincount = 0 # count per bin
# currbin = 0 # current bin; bin number of intensity i is floor(i/binwidth)

# for index in range(len(sandpix)):
# 	i = sandpix[index]
# 	if i/binwidth == currbin:
# 		bincount++
# 	else:
# 		error = 

# img = cv2.imread('./sample_images/1.jpg',0)

# win_size = 64
# windows = sliding_window(img, win_size, (win_size, win_size))
# for (col, row, window) in windows:
# 	if window.shape[0] != win_size or window.shape[1] != win_size:
# 		continue
# 	pixels = sorted(np.matrix(window).getA1())