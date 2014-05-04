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
                #start pitch type
                pitcher = m['@pitcher']
                pitch = m['pitch']
                pitch_possibilities = [['FF','FA'],['FT'],['FC'],['SI','FS'],['SF'],['SL'],['CH'],['CB','CU'],['KC'],['KN'],['EP']]
                #end pitch type
                if pitcher not in dic:
                    dic[pitcher] = {}
                    #start pitch type
                    dic[pitcher]['pitch_type'] = {}
                    pitch_type = dic[pitcher]['pitch_type']
                    #start left handed or right handed
                    dic[pitcher]['handedness'] = m['@p_throws']
                    #end left handed or right handed
                    for poss in pitch_possibilities:
                        pitch_type[poss[0]] = 0
                    pitch_type['total'] = 0.0
                    #end pitch type
                if isinstance(pitch, dict): #this is because if there is only one throw, then the data is in a dictionary instead of a list of dictionaries
                    #start pitch type
                    pt = pitch['@pitch_type']
                    for poss in pitch_possibilities:
                        for t in poss:
                            if pt == t:
                                pitch_type[poss[0]] += 1
                                pitch_type['total'] += 1
                    #end pitch type
                else:    #here, because there is more than one throw, the data is in a list of dictionaries
                    for pi in pitch:
                        #start pitch type
                        pt = pi['@pitch_type']
                        for poss in pitch_possibilities:
                            for t in poss:
                                if pt == t:
                                    pitch_type[poss[0]] += 1
                                    pitch_type['total'] += 1
                        #end pitch type
                        
                        
    for player, attributes in dic.items():
        #start pitch type
        pitch_type_dic = attributes['pitch_type']

        pitch_total = pitch_type_dic['total']
        #end pitch type
        #start handedness
        handedness = attributes['handedness']
        #end handedness
        vector = []
        #start pitch type
        pitch_type_list = ['FF','FT','FC','SI','SF','SL','CH','CB','KC','KN','EP']
        for ty in pitch_type_list:
            vector.append(pitch_type_dic[ty] / pitch_total)
        #end pitch type
        #start handedness
            if handedness == 'L':
                vector.append(1)
                vector.append(0)
            elif handedness == 'R':
                vector.append(0)
                vector.append(1)
        #end handedness
        print (player, vector)
        vector = np.array(vector, float)
        tup = (player, vector)
        results.append(tup)
    return results 

results = produce_results()
pickle.dump(results, open("results.p", "wb"))
