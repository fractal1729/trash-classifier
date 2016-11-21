import math
import csv
import time
import cv2
import numpy as np
from numpy import genfromtxt
import random
import operator
from Testing_Grounds.helpers import compressJPG
from sklearn.neural_network import MLPClassifier


COLOR_THRESH = 150
EDGE_MIN_THRESH = 100
EDGE_MAX_THRESH = 200
TEST_CASE_SIZE = 50
NUM_TRAINING_IMAGES = 300
RESIZE_FACTOR = 0.5

def featuresForImage(img):
    color = cv2.cvtColor(colorDetect(img, COLOR_THRESH), cv2.COLOR_BGR2GRAY)
    edge = cv2.Canny(img, EDGE_MIN_THRESH, EDGE_MAX_THRESH)
    #edge = cv2.cvtColor(cv2.Canny(img,EDGE_MIN_THRESH,EDGE_MAX_THRESH), cv2.COLOR_BGR2GRAY)
    grayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


    return [color, edge, grayscale]

def extractFeatures(img, coords):
    window_features = [[]]*len(coords)
    feat_imgs = featuresForImage(img)

    for i in range(len(coords)):
        window_features[i] = np.array([crop(feat_imgs[0],coords[i]).flatten(), crop(feat_imgs[1],coords[i]).flatten(), crop(feat_imgs[2],coords[i]).flatten()]).flatten()

    return window_features

def crop(img, coords):
    crop_img = img[coords[0]:coords[0]+coords[2], coords[1]:coords[1]+coords[2]]
    return crop_img

def colorDetect(img, thresh):

    height, width, channels = img.shape;
    sand = [194, 178, 128];
    new_image = np.zeros((height,width,channels), np.uint8);

    for i in range(height):
        for j in range(width):
			px = img[i][j]
			dist_sand = math.sqrt(math.pow((px[0] - sand[0]),2) + math.pow((px[1] - sand[1]),2) + math.pow((px[2] - sand[2]),2))
			# dist_seaweed = math.sqrt(math.pow((px[0] - seaweed[0]),2) + math.pow((px[1] - seaweed[1]),2) + math.pow((px[2] - seaweed[2]),2))
			if dist_sand > thresh:
				new_image[i][j] = [255,255,255]

	return new_image

def getCoords(row):
    index = 1
    coords = []
    while (index < len(row)) and (not math.isnan(row[index])) :
        coords.append([row[index],row[index+1],row[index+2],row[index+3]])
        index = index + 4
    return coords

def generateNegativeTestCases(coords, width, height, size, count):
    negCoords = [];
    for i in range(0, count):
        y = random.randint(0,height-1-size)
        x = random.randint(0,width-1-size)
        #confirm that this does not overlap of the coordinates
        foundoverlap = False
        for coord in coords:
            if x < coord[1] + coord[3] and x + size > coord[1] and y < coord[0] + coord[2] and y + size  > coord[0]:
                foundoverlap = True
        if not foundoverlap:
            negCoords.append([y, x, size, 0]);

    return negCoords;

#coords = An array of 4-element arrays of x, y, h, w
## This version is better but it needs to get boxes down to all the same size
# def generatePositiveTestCases(coords, w, h, count):
#     finalcoords = [];
#     for coord in coords:
#         top = coord[0]
#         left = coord[1]
#         height = coord[2]
#         width = coord[3]
#         size = max(width, height)
#
#         for x in range(0, count):
#             additionalsize = random.randint(0, int(size*2))
#             ntop = top - random.randint(0, additionalsize)
#             nleft = left - random.randint(0, additionalsize)
#
#             if(ntop >=0 and nleft >=0 and ntop+size+additionalsize < h and  nleft+size+additionalsize < w):
#                 finalcoords.append([int(ntop),int(nleft), int(size+additionalsize), 1])
#
#     return finalcoords

def generatePositiveTestCases(coords, width, height, size, count):
    posCoords = [];
    while len(posCoords) < count:

        y = random.randint(0,height-1-size)
        x = random.randint(0,width-1-size)

        for coord in coords:
            if x < coord[1] + coord[3] and x + size > coord[1] and y < coord[0] + coord[2] and y + size  > coord[0]:
                posCoords.append([y, x, size, 0]);
                break

    return posCoords;


filePrefix = "allpics/"


pictureList = []


count = 0
with open('trainingdata.csv', 'rb') as csvfile:
     reader = csv.DictReader(csvfile)
     print(reader)
     for row in reader:
         if count < NUM_TRAINING_IMAGES:
            count = count + 1
            img = cv2.imread(filePrefix + row["1"] )
            pictureList.append(img)


#unroll pictures and pop them into
coordinates = genfromtxt('trainingdata.csv', delimiter=',')
X = []
Y = []
print "Extracting Features from ", len(pictureList), " pictures..."
startTime = time.time() * 1000

for i in range(0, len(pictureList)):

    coords = getCoords(coordinates[i + 1])
    img = pictureList[i]
    if img is None or coords is None or len(coords) == 0:
        print ".."
        continue;
    # img = compressJPG(img, RESIZE_FACTOR)
    print "Compressed Image Size: (", len(img[0]), ", ", len(img), ")"
    width =  pictureList[i].shape[0]
    height = pictureList[i].shape[1]

    # Generate test cases based on the coordinates, the width and height of the picture, and the size and count of the boxes
    positivetestcases = generatePositiveTestCases(coords, width, height, TEST_CASE_SIZE, 100)
    negativetestcases = generateNegativeTestCases(coords, width, height, TEST_CASE_SIZE, 150)

    testcases = positivetestcases+negativetestcases

    X = X + extractFeatures(img, testcases)

    #Label ones and zeros
    Y = Y + np.append([1]*len(positivetestcases), [0]*len(negativetestcases)).tolist()
    print "."

print "Extracted Features in ", (time.time() * 1000)-startTime, " milliseconds\n"
print "Number of Training Data: ", len(X)
print "Number of Features: ", len(X[0])
print "Number of Positive Training Data: ", Y.count(1)
print "Number of Negative Training Data: ", Y.count(0),"\n"

print "Training Neural Network..."
X = np.array(X)
Y = np.array(Y)
numTrainData = 0.8 * len(X)
Xtrain = X[0:numTrainData]
Ytrain = Y[0:numTrainData]
Xtest = X[numTrainData+1:len(X)-1]
Ytest =Y[numTrainData+1:len(Y)-1]
print "Lengths X, Xtrain, Xtest: ", len(X), ", ", len(Xtrain), ", ", len(Xtest)

startTime = time.time() * 1000
#Run the Neural Net!
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                         hidden_layer_sizes=(5, 2), random_state=1)
clf.fit(Xtrain, Ytrain)
print(".\n.\n.")
MLPClassifier(activation='relu', alpha=1e-05, batch_size='auto',
           beta_1=0.9, beta_2=0.999, early_stopping =False,
           epsilon=1e-08, hidden_layer_sizes=(5, 2), learning_rate='constant',
           learning_rate_init=0.001, max_iter=200, momentum=0.9,
           nesterovs_momentum=True, power_t=0.5, random_state=1, shuffle=True,
           solver='lbfgs', tol=0.0001, validation_fraction=0.1, verbose=False,
           warm_start=False)

print "Time taken to train: ", (time.time() * 1000)-startTime, " milliseconds\n"
predictions = clf.predict(Xtest)
print "Predicting on ", len(Xtest), "cases"
print "Results: ", predictions
print "Expected Results: ", Ytest
print "Accuracy: ", (float((np.array(predictions) - np.array(Ytest)).tolist().count(0))/float(len(Ytest)))*100, "%"
