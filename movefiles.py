import os
import sys
import glob
import subprocess
import shutil
#from sets import Set

#copy files from games that match "inning_all.xml" to folder in main directory

fdepth = glob.glob('games/*/*/*/*/*')
print fdepth
ddepth = filter(lambda f: os.path.isdir(f), fdepth)
i = 0
sdepth = set()
for x in ddepth:
    sdepth.add(x)
for file in ddepth:
    innings_all = os.path.join(file, "inning_all.xml")
    if os.path.isfile(innings_all) == True:
        string = 'cp ' + innings_all + ' flat_games_all_2/inning_all_2_' + str(i) + '.xml'
        subprocess.call(string, shell=True)
        print "another one (innings_all) bites the dust"
        
    else:
        for number in range(1,21):
            inning = os.path.join(file, "inning_" + str(number) + ".xml")
            if os.path.isfile(inning) == True:
                string = 'cp ' + inning + ' flat_games_all_2/inning_2_' + str(i) + "_" + str(number) + '.xml'
                subprocess.call(string, shell=True)
                print "another one (inning) bites the dust"         
            
    i = i + 1            