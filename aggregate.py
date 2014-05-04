import os, json
import numpy as np
import pickle



def get_data(file_name):
    f = open(file_name, "r+")   
    data = json.load(f)
    f.close()
    return data

def produce_results(dic, file_name):
    #structure of each pitcher: tuple (pitcher_id, [vector of attributes])
    # results = [] #this will be the list of pitchers
    # dic = {} #this will be our working dictionary of pitchers that will be transcribed to the results list
    data = get_data(file_name)['game']
    inning = data['inning']
    if isinstance(inning, dict):
        inning = [inning]
    for inn in inning:
        tb = []
        if 'top' in inn.keys():
            top = inn['top']
            tb.append(top)
        if 'bottom' in inn.keys():
            bottom = inn['bottom']
            tb.append(bottom)
        for x in tb:
            if x != None:
                if 'atbat' in x.keys():
                    l = x['atbat']
                    if isinstance(l, dict):
                        l = [l] 
                    for m in l:
                        #start pitch type
                        pitcher = m['@pitcher']
                        if 'pitch' in m.keys():
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
                            else:
                                pitch_type = dic[pitcher]['pitch_type']
                            if isinstance(pitch, dict): #this is because if there is only one throw, then the data is in a dictionary instead of a list of dictionaries
                                pitch = [pitch]
                            for pi in pitch:
                                #start pitch type
                                # print pi
                                if '@pitch_type' in pi.keys():
                                    pt = pi['@pitch_type']
                                    for poss in pitch_possibilities:
                                        for t in poss:
                                            if pt == t:
                                                pitch_type[poss[0]] += 1
                                                pitch_type['total'] += 1
                                #end pitch type
                          
                                          

    return dic

def dict_to_list(dic):   
    results = []
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
        if len(vector) != 13:
            print "VECTOR IS NOT CORRECT LENGTH"
            exit()
        vector = np.array(vector, float)
        tup = (player, vector)
        results.append(tup)
    return results 

def main_function():
    dictionary = {}
    curr = os.path.dirname(os.path.realpath(__file__))
    folder = os.path.join(curr, "june_data")
    for root, dirs, filenames in os.walk(folder):
        for game_file in filenames:
            name = os.path.join(folder, game_file)
            if name.endswith('.json'):
                dictionary = produce_results(dictionary, name)
            # f = open(os.path.join(folder, filenames), "r+")    
    # results = []
    # results = produce_results()
    results = dict_to_list(dictionary)
    pickle.dump(results, open("results.p", "wb"))

main_function()
