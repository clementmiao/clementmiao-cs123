from xml2json import xml2json
import os
import sys
import glob
import subprocess
#from sets import Set

fdepth = glob.glob('*/*/*/*/*/*')
ddepth = filter(lambda f: os.path.isdir(f), fdepth)

i = 0
sdepth = set()
for x in ddepth:
    sdepth.add(x)
for file in ddepth:
    innings = os.path.join(file, "inning_all.xml")
    if "month_06" in innings:
        string = 'xml2json -t xml2json -o june_data/inning_all_' + str(i) + '.json ' + innings
        subprocess.call(string, shell=True)
        i = i + 1
               
            
