import cv2
import numpy

def vectorizer(filename, x, y, width, height):
  img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE);
  crop_img = img[y:y+h, x:x+w];
  crop_img.flatten()
  return crop_img
