import os
import sys
import glob
import subprocess
import json
#import numpy as np
import xml.etree.ElementTree as ET
#from sets import Set


def playerTeam():
    d = {}
    pa = '/home/charlie/clemetnmiao-cs123'
    for root, dirs, filenames in os.walk('players_07'):
        for f in filenames:
            path = os.path.join(pa, 'players_07', f)
            print(path)
            print(os.path.abspath(f))
            tree = ET.parse(path)
            game = tree.getroot()
            for team in game:
                name = team.get('name')
                for player in child:
                    pid = player.get('id')
                    d[pid] = name
    for p in d:
        print("This should work " + p + " " + d[p])
            
