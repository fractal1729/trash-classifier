import sys
import cv2
import numpy as np
from matplotlib import pyplot as plt

COLOR_THRESH = 150
EDGE_MIN_THRESH = 100
EDGE_MAX_THRESH = 200

def features(img):
    color = cv2.cvtColor(detect(img, COLOR_THRESH), cv2.COLOR_BGR2GRAY).flatten()
    edge = cv2.cvtColor(cv2.Canny(img,EDGE_MIN_THRESH,EDGE_MAX_THRESH), cv2.COLOR_BGR2GRAY).flatten()
    grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).flatten()

    return [color, edge, grayscale]