import os
import sys
import subprocess
#import numpy as np
import math

def readPlayerFile(file_name, d):
    f = open(file_name, "r+")
    d['total'] = 0
    for line in f.readlines():
        att = []
        arr = line.strip().split(',')
        first_element = arr[0].split("\t") 
        pid = first_element[0]
        d['total'] += int(first_element[1])
        arr = arr[1:]
        for i in range(0, len(arr)/2):
            att.append((int(arr[2*i]), int(arr[2*i + 1])))
        if pid not in d:
            d[pid] = att
        else:
            for i in range(0, len(att)):
                d[pid][i][0] += att[i][0]
                d[pid][i][1] += att[i][1]
    f.close()
    return d

def score(train, test):
    s = 0.0
    for player in test:

        if player in train and player != 'total':
            for i in range(0, len(test[player])):
                test_element = test[player][i]
                train_element = train[player][i]
                test_0 = test_element[0]
                test_1 = test_element[1]
                train_0 = train_element[0]
                train_1 = train_element[1]
                if test_1 != 0 and train_1 != 0:
                    testAvg = 1.0*test_0/test_1
                    trainAvg = 1.0*train_0/train_1
                else:
                    trainAvg = 0.0
                    testAvg = 0.0
                s += 1.0*test_1#*abs(trainAvg - testAvg)

    return 1 - s / test['total']

def accuracy(folder1, testFile):
    playersTrain = {}
    #for each of the training files:
    playersTrain = readPlayerFile(folder1, playersTrain)
    #read in test file
    playersTest = {}
    playersTest = readPlayerFile(testFile, playersTest)
    s = score(playersTrain, playersTest)
    print("Score: " + str(s))
    

accuracy(sys.argv[1], sys.argv[2])
        
