from xml2json import xml2json
import os
import sys
import glob
import subprocess
#from sets import Set

fdepth = glob.glob('*/*/*/*/*/*')
ddepth = filter(lambda f: os.path.isdir(f), fdepth)
#print ddepth
#cur = os.path.dirname(os.path.realpath(__file__))
#path = 'games/year_2011/month_06'
#path = os.path.join(cur, path)
i = 0
sdepth = set()
for x in ddepth:
    sdepth.add(x)
#print len(ddepth)
#print len(sdepth)
#first = ddepth[0]
#innings = os.path.join(first, "inning_all.xml")
#os.system('xml2json -t xml2json -o inning_all_' + str(i) + '.json ' + innings)
for file in ddepth:
    innings = os.path.join(file, "inning_all.xml")
    if "month_06" in innings:
        string = 'xml2json -t xml2json -o inning_all_' + str(i) + '.json ' + innings
        print i
        subprocess.call(string, shell=True)
        i = i + 1
    #os.system('xml2json -t xml2json -o inning_all_' + str(i) + '.json ' + innings)
    #    path1 = os.path.join(path, day)
    #    print path1
        #for subroot, subsubFolders, subfiles in os.walk(path1):
            #for game in subsubFolders:
                #innings = os.path.join(path1, game, "inning_all.xml")
                #print(innings)
                #os.system('xml2json -t xml2json -o inning_all.json ' + innings)
               
            
