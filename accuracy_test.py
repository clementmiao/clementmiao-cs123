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
        att['total'] = arr[1]
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
        s += abs(train[player][0]/train[player][1] - test[player][0]/test[player][1])
    return s

def accuracy(folder1, testFile):
    playersTrain = {}
    #for each of the training files:
    playersTrain = readPlayerFile(file_name, playersTrain)
    #read in test file
    playersTest = {}
    playersTest = readPlayerFile(test_file, playersTest)
    s = score(playersTrain, playersTest)
    print("Score: " + s)
    

accuracy(sys.argv[1], sys.argv[2])
        
