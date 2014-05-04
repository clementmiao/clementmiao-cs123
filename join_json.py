import os,shutil

curr = os.path.dirname(os.path.realpath(__file__))
f=open(os.path.join(curr, "input_file.json"),"a")
input_folder = os.path.join(curr, "june_data")
for r,d,fi in os.walk(input_folder):
    for files in fi:
        if files.endswith(".json"):                         
            g=open(os.path.join(r,files))
            shutil.copyfileobj(g,f)
            g.close()
f.close()
 