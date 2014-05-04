import os, json
import numpy as np
import pickle


curr = os.path.dirname(os.path.realpath(__file__))
f=open(os.path.join(curr, "test.json"),"r+")

def get_data():
    data = json.load(f)
    f.close()
    return data

def produce_results():
    #structure of each pitcher: tuple (pitcher_id, [vector of attributes])
    results = [] #this will be the list of pitchers
    dic = {} #this will be our working dictionary of pitchers that will be transcribed to the results list
    data = get_data()['game']
    inning = data['inning']
    for inn in inning:
        top = inn['top']
        bottom = inn['bottom']
        for x in [top, bottom]:
            l = x['atbat']
            for m in l:
                pitcher = m['@pitcher']
                pitch = m['pitch']
                pitch_possibilities = [['FF','FA'],['FT'],['FC'],['SI','FS'],['SF'],['SL'],['CH'],['CB','CU'],['KC'],['KN'],['EP']]
                if pitcher not in dic:
                    dic[pitcher] = {}
                    dic[pitcher]['pitch_type'] = {}
                    pitch_type = dic[pitcher]['pitch_type']
                    # pitch_type_list = ['FF','FT','FC','SI','SF','SL','CH','CB','KC','KN','EP']
                    for poss in pitch_possibilities:
                        pitch_type[poss[0]] = 0
                    pitch_type['total'] = 0.0
                # pitch_possibilities = [['FF','FA'],['FT'],['FC'],['SI','FS'],['SF'],['SL'],['CH'],['CB','CU'],['KC'],['KN'],['EP']]
                if isinstance(pitch, dict):
                    pt = pitch['@pitch_type']
                    for poss in pitch_possibilities:
                        for t in poss:
                            if pt == t:
                                pitch_type[poss[0]] += 1
                                pitch_type['total'] += 1
                else:    
                    for pi in pitch:
                        pt = pi['@pitch_type']
                        for poss in pitch_possibilities:
                            for t in poss:
                                if pt == t:
                                    pitch_type[poss[0]] += 1
                                    pitch_type['total'] += 1
                        
                        
    for player, attributes in dic.items():
        pitch_type_dic = attributes['pitch_type']
        pitch_total = pitch_type_dic['total']
        vector = []
        pitch_type_list = ['FF','FT','FC','SI','SF','SL','CH','CB','KC','KN','EP']
        for ty in pitch_type_list:
            vector.append(pitch_type_dic[ty] / pitch_total)
        print (player, vector)
        vector = np.array(vector, float)
        tup = (player, vector)
        results.append(tup)
    return results 

results = produce_results()
pickle.dump(results, open("results.p", "wb"))
