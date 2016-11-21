import math
import csv
import time
import cv2
import numpy as np
from numpy import genfromtxt

import operator
from Testing_Grounds.helpers import compressJPG, generatePositiveTestCases, generateNegativeTestCases, getCoords, extractFeatures
from sklearn.neural_network import MLPClassifier


NUM_TRAINING_IMAGES = 1000

filePrefix = "allpics/"
pictureList = []

# Opens trainingdata.csv and goes through NUM_TRAINING_IMAGES rows and gets the image
count = 0
with open('trainingdata.csv', 'rb') as csvfile:
     reader = csv.DictReader(csvfile)
     for row in reader:
         print("Reading Row...")
         if count < NUM_TRAINING_IMAGES:
            count = count + 1
            img = cv2.imread(filePrefix + row["1"] )
            pictureList.append(img)


#unroll pictures and pop them into a list
coordinates = genfromtxt('trainingdata.csv', delimiter=',')
X = []
Y = []
print "Extracting Features from ", len(pictureList), " pictures..."
startTime = time.time() * 1000

for i in range(0, len(pictureList)):

    coords = getCoords(coordinates[i + 1])
    img = pictureList[i]
    if img is None or len(img) == 0 or len(img[0]) == 0 or coords is None or len(coords) == 0:
        print ".."
        continue;
    # img = compressJPG(img, RESIZE_FACTOR)
    # print "Compressed Image Size: (", len(img[0]), ", ", len(img), ")"
    width =  pictureList[i].shape[0]
    height = pictureList[i].shape[1]

    # Generate test cases based on the coordinates, the width and height of the picture, and the size and count of the boxes
    positivetestcases = generatePositiveTestCases(coords, width, height, 50, 200, 30)
    negativetestcases = generateNegativeTestCases(coords,width, height, 50, 200, 100)

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
print(X[0:10])
numTrainData = 0.8 * len(X)
Xtrain = X[0:numTrainData]
Ytrain = Y[0:numTrainData]
Xtest = X[numTrainData+1:len(X)-1]
Ytest =Y[numTrainData+1:len(Y)-1]
print "Lengths X, Xtrain, Xtest: ", len(X), ", ", len(Xtrain), ", ", len(Xtest)

startTime = time.time() * 1000
#Run the Neural Net! Basically Magic.
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

#Check Predictions against real values
print "Time taken to train: ", (time.time() * 1000)-startTime, " milliseconds\n"
predictions = clf.predict(Xtest)
print "Predicting on ", len(Xtest), "cases"
print "Results: ", predictions
print "Expected Results: ", Ytest
print "Accuracy: ", (float((np.array(predictions) - np.array(Ytest)).tolist().count(0))/float(len(Ytest)))*100, "%"
