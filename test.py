import helpers
import cv2

img = compressJPG(cv2.imread("sample_images/1.jpg"), 10)
plt.imshow(img, cmap='gray')
plt.show()