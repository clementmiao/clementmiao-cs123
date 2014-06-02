import os
import sys
import glob
import subprocess
import json
import numpy as np
import xml.etree.ElementTree as ET
#from sets import Set


fdepth = glob.glob('*/*/*/*/*')
ddepth = filter(lambda f: os.path.isdir(f), fdepth)
i = 0
sdepth = set()
for x in ddepth:
    sdepth.add(x)
for file in ddepth:
    tree = ET.parse('players.xml')
    root = tree.getroot()
    for child in root:
    
    string = 'xml2json -t xml2json -o json/' + str(i) + '.json ' + players
    subprocess.call(string, shell=True)
    i = i + 1
