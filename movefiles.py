import os
import sys
import glob
import subprocess
import shutil
#from sets import Set

#copy files from games that match "inning_all.xml" to folder in main directory

fdepth = glob.glob('*/*/*/*/*/*')
ddepth = filter(lambda f: os.path.isdir(f), fdepth)
i = 0
sdepth = set()
for x in ddepth:
    sdepth.add(x)
for file in ddepth:
    innings = os.path.join(file, "inning_all.xml")
    # print innings
    string = 'cp ' + innings + ' flat_games/inning_all_' + str(i) + '.xml'
    subprocess.call(string, shell=True)
    print "another one hits the dust"
    i = i + 1
               
            
