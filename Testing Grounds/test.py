# Standard imports
import cv2
import numpy as np
from matplotlib import pyplot as plt
 
# Read image
img = cv2.imread("sample_images/1.jpg", cv2.IMREAD_GRAYSCALE)
original = cv2.imread("sample_images/1.jpg", cv2.IMREAD_GRAYSCALE)

plt.subplot(131),plt.imshow(original)
plt.title('Original Image'), plt.xticks([]), plt.yticks([])

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector()
 
# Detect blobs.
keypoints = detector.detect(img)
 
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
img_with_keypoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

plt.subplot(132),plt.imshow(img)
plt.title('Blob Image'), plt.xticks([]), plt.yticks([])
 
edges = cv2.Canny(img,100,200) # run the actual edge detection

plt.subplot(133),plt.imshow(edges)
plt.title('Edges'), plt.xticks([]), plt.yticks([])

plt.show()