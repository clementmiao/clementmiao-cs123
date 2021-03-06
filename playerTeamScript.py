import os
import sys
import glob
import subprocess
#import numpy as np
import xml.etree.ElementTree as ET
#from sets import Set


def playerTeam():
    d = {}
    for root, dirs, filenames in os.walk('players_07'):
        for f in filenames:
            path = os.path.join('players_07', f)
            tree = ET.parse(path)
            game = tree.getroot()
            for team in game:
                if(team.tag != 'umpires'):
                    name = team.get('name')
                    #print("name: " + name)
                    for player in team:
                        if(player.tag != 'coach'):
                            pid = player.get('id')
                            last = player.get('last')
                            first = player.get('first')
                            #print("ID: " + pid)
                            d[pid] = (name, first + " " + last)
    for p in d:
        print("This should work " + p + " " + d[p][0] + " " + d[p][1])
            
