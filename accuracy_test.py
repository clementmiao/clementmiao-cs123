import os
import sys
import subprocess
#import numpy as np
import math

def readPlayerFile(file_name, d):
    f = open(file_name, "r+")
    for line in f.readlines():
        att = []
        arr = line.split(',')
        #att['total'] = arr[1]
        for i in range(0, len(arr)/2 - 1):
            att.append((arr[2*i + 2], arr[2*i + 1 + 2]))
        if arr[0] not in d:
            d[arr[0]] = att
        else:
            for i in range(0, len(att)):
                d[arr[0]][i][0] += att[i][0]
                d[arr[0]][i][1] += att[i][1]
    f.close()
    return d

def score(train, test):
    s = 0.0
    for player in test:

        #s += abs((double)train[player][0]/train[player][1] - (double)test[player][0]/test[player][1])

        if player in train:
            for i in test[player]:
                element_0 = int(i[0])
                element_1 = int(i[1])
                if element_0 != 0 and element_1 != 0:
                    trainAvg = 1.0*element_0]/train[player][element_1]
                    testAvg = (1.0*test[player][element_0]/test[player][element_1)
                else:
                    trainAvg = 0.0
                    testAvg = 0.0
                s += test[player][i[1]]*abs(trainAvg - testAvg)

    return s

def accuracy(folder1, testFile):
    playersTrain = {}
    #for each of the training files:
    playersTrain = readPlayerFile(folder1, playersTrain)
    #read in test file
    playersTest = {}
    playersTest = readPlayerFile(testFile, playersTest)
    s = score(playersTrain, playersTest)
    print("Score: " + s)
    

accuracy(sys.argv[1], sys.argv[2])
        
