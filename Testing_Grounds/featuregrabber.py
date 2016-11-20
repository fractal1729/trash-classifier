#TODO for Gautam
import cv2
FINAL_SIZE = 16;

def convertToFeatures(testcases, img):
    gray_scale = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY);

    X = [];
    Y = [];
    #now go through each of the testcases, and generate the features
    for c in testcases:
        cropped = gray_scale[c[0]:c[0]+c[2],c[1]:c[1]+c[2]];
        resized_image = cv2.resize(cropped, (FINAL_SIZE, FINAL_SIZE))
        # cv2.imshow('image',resized_image)
        print resized_image
        # cv2.waitKey(0)
    return True
